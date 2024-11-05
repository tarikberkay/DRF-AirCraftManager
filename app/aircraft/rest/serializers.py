from rest_framework import serializers
from aircraft.models import *


class AircraftPartSerializer(serializers.ModelSerializer):
    class Meta:
        model = AircraftPart
        fields = ['id', 'aircraft', 'part', 'quantity']

    def validate(self, data):
        # Parça ilgili uçağa ait olduğu için başka bir uçakta kullanılamaz
        if AircraftPart.objects.filter(part=data['part']).exclude(aircraft=data['aircraft']).exists():
            raise serializers.ValidationError(
                "Bu parça zaten başka bir uçakta kullanılıyor.")
        return data

    def create(self, validated_data):
        # Parça envanterde mevcut değilse veya yeterli değilse hata veriyoruz.
        part = validated_data['part']
        quantity_needed = validated_data['quantity']
        if part.quantity < quantity_needed:
            raise serializers.ValidationError(
                f"Stokta yeterli {part.name} parçası bulunmamaktadır.")

        # Parçayı stoktan düşürüp ve AircraftPart kaydı oluşturuyoruz.
        part.quantity -= quantity_needed
        part.save()
        return super().create(validated_data)


class AircraftSerializer(serializers.ModelSerializer):
    parts = AircraftPartSerializer(many=True, read_only=True)

    class Meta:
        model = Aircraft
        fields = ['id', 'model', 'assembled', 'parts']

    def assemble_aircraft(self, instance):
        required_parts = {'KANAT', 'GÖVDE', 'KUYRUK', 'AVİYONİK'}
        current_parts = {part.type for part in instance.specific_parts.all()}

        # Montaj sırasında eksik parçaları kontrol ediyoruz.
        if required_parts == current_parts:
            instance.assembled = True
            instance.save()
            return "Uçak başarıyla monte edildi!"
        else:
            missing_parts = required_parts - current_parts
            raise serializers.ValidationError(
                f"Montaj başarısız. Eksik parçalar: {', '.join(missing_parts)}")


class PersonelSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    team = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Personel
        fields = ['id', 'user', 'team', 'name', 'phone']


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ['id', 'name', 'part_type']


class PartAllSerializer(serializers.ModelSerializer):
    class Meta:
        model = Part
        fields = ['id', 'name', 'type']


class PartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Part
        fields = ['id', 'type', 'quantity']
        read_only_fields = ['quantity']

    def validate(self, data):
        # Sadece yetkili takımın kendi parça tipini üretmesini sağlıyoruz.
        team = self.context['request'].user.personnel.team
        if team.name != 'MONTAJ_TAKIMI' and team.part_type != data['type']:
            raise serializers.ValidationError(
                "Bu takım sadece kendi parça tipini üretebilir.")
        return data

    def create(self, validated_data):
        part_type = validated_data.get('type')

        # Aynı tipte bir parça mevcut mu diye kontrol ediyoruz.
        part, created = Part.objects.get_or_create(
            type=part_type, defaults={'quantity': 1})

        if not created:  # Zaten mevcutsa
            part.quantity += 1  # quantity değerini arttırıyoruz
            part.save()

        return part

from rest_framework import serializers
from authentication.models import CustomUser

# TODO
from django.contrib.auth.tokens import default_token_generator  # TODO
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.urls import reverse
from django.conf import settings
from django.core.exceptions import ValidationError
from rest_framework.generics import get_object_or_404


from aircraft.models import Personel, Team
from aircraft.rest.serializers import TeamSerializer


# from django.contrib.auth import get_user_model

# User = get_user_model()


class UserRegisterSerializer(serializers.ModelSerializer):
    # team = serializers.PrimaryKeyRelatedField(queryset=Team.objects.all(), required=True)
    team = serializers.IntegerField(required=False)

    class Meta:
        model = CustomUser
        fields = ('id', 'email', 'password', 'name', 'phone', 'is_personel', 'team')
        read_only_fields = ['id']
        extra_kwargs = {'password': {'write_only': True},
                        'email': {'required': True}}

    def create(self, validated_data):
        try:
            email = validated_data.get('email')
            name = validated_data.pop('name', None)
            phone = validated_data.pop('phone')
            is_personel = validated_data.pop('is_personel', False)
            team = validated_data.pop('team', None)
        except Exception as e:
            print("Error occurred: {e}")
            raise

        user = CustomUser.objects.create(
            email=email,
            name=name,
            phone=phone,
            is_personel=is_personel,
        )

        user.set_password(validated_data.pop('password'))
        user.save()

        if user.is_personel:
            personel = Personel.objects.create(
                user=user,
                name=name,
                phone=phone,
                team_id=team
            )
        return user


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate_old_password(self, value):
        request = self.context.get('request')
        if not request.user.check_password(value):
            raise ValidationError("Old password is not correct")
        return value

    def validate_new_password(self, value):
        return value

    def save(self, **kwargs):
        request = self.context.get('request')
        user = request.user
        user.set_password(self.validated_data['new_password'])
        user.save()
        return user

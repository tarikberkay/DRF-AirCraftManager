from django.db import models
from django.contrib.auth.models import User
from django.conf import settings


class Personel(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="personel"
    )
    team = models.ForeignKey(
        'Team', on_delete=models.CASCADE, related_name='personel', null=True, blank=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return self.user.name if self.user else "No User"


# Uçak Modelleri
class Aircraft(models.Model):
    MODEL_CHOICES = [
        ('TB2', 'TB2'),
        ('TB3', 'TB3'),
        ('AKINCI', 'AKINCI'),
        ('KIZILELMA', 'KIZILELMA')
    ]
    model = models.CharField(max_length=50, choices=MODEL_CHOICES, unique=True)
    assembled = models.BooleanField(default=False)  # Montaj durumu
    parts = models.ManyToManyField(
        'Part', through='AircraftPart', related_name='aircrafts')

    def __str__(self):
        return self.model

    def assemble_aircraft(self):
        # Montaj takımı tüm parçaları birleştirirken eksik parça kontrolü yapar
        required_parts = {'KANAT', 'GÖVDE', 'KUYRUK', 'AVİYONİK'}
        current_parts = {part.type for part in self.specific_parts.all()}

        if required_parts == current_parts:
            self.assembled = True
            self.save()
            return "Aircraft assembled successfully!"
        else:
            missing_parts = required_parts - current_parts
            return f"Assembly failed. Missing parts: {', '.join(missing_parts)}"


# Parça Modelleri
class Part(models.Model):
    PART_TYPE_CHOICES = [
        ('KANAT', 'Kanat'),
        ('GÖVDE', 'Gövde'),
        ('KUYRUK', 'Kuyruk'),
        ('AVİYONİK', 'Aviyonik')
    ]
    name = models.CharField(max_length=50, blank=True, null=True)
    type = models.CharField(max_length=20, choices=PART_TYPE_CHOICES)
    aircraft = models.ForeignKey(
        Aircraft, on_delete=models.CASCADE, related_name='specific_parts', null=True, blank=True)
    team = models.ForeignKey(
        'Team', on_delete=models.CASCADE, related_name='parts', null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)  # Stok Miktarı

    def __str__(self):
        if self.name:
            return f"{self.name} ({self.type})"
        return self.type

    def produce_part(self, amount):
        # Üretim işlemi için miktarı artırır
        self.quantity += amount
        self.save()

    def recycle_part(self, amount):
        # Geri dönüşüm (silme) işlemi için miktarı azaltır
        if self.quantity >= amount:
            self.quantity -= amount
            self.save()
        else:
            raise ValueError("Not enough parts in inventory for recycling.")


# Takım Modelleri
class Team(models.Model):
    TEAM_NAME_CHOICES = [
        ('KANAT_TAKIMI', 'Kanat Takımı'),
        ('GÖVDE_TAKIMI', 'Gövde Takımı'),
        ('KUYRUK_TAKIMI', 'Kuyruk Takımı'),
        ('AVİYONİK_TAKIMI', 'Aviyonik Takımı'),
        ('MONTAJ_TAKIMI', 'Montaj Takımı')
    ]
    name = models.CharField(
        max_length=50, choices=TEAM_NAME_CHOICES, unique=True)
    part_type = models.CharField(
        max_length=20, choices=Part.PART_TYPE_CHOICES, null=True, blank=True)

    def __str__(self):
        return self.name

    def can_produce_part(self, part_type):
        return self.part_type == part_type or self.name == 'MONTAJ_TAKIMI'


# Uçak ve Parça Arasındaki İlişki
class AircraftPart(models.Model):
    aircraft = models.ForeignKey(Aircraft, on_delete=models.CASCADE)
    part = models.ForeignKey(Part, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)  # Parça sayısı

    class Meta:
        unique_together = ('aircraft', 'part')

    def __str__(self):
        return f"'{self.aircraft.model}' de {self.quantity} tane '{self.part.type}' parçası var."

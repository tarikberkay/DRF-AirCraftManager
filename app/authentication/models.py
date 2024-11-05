from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models
from django.contrib.auth.models import PermissionsMixin, AbstractUser
from typing import Optional
from django.conf import settings


GENDER_CHOICES = (
    (1, "Man"),
    (2, "Woman"),
)


class CustomUserManager(BaseUserManager):
    def create_user(self, email, name=None, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        if not name:
            name = "unknown"
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, name=name, password=password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=100, unique=True)
    name = models.CharField(max_length=200, blank=True,
                            null=True)  # Kullanıcı adı
    gender = models.IntegerField(
        choices=GENDER_CHOICES, blank=True, null=True)  # Cinsiyet
    phone = models.CharField(max_length=30, blank=True,
                             null=True)  # Telefon numarası
    is_admin = models.BooleanField(default=False)  # Admin yetkisi
    is_personel = models.BooleanField(default=False)  # Personel durumu
    is_active = models.BooleanField(default=True)  # Aktif kullanıcı durumu
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)  # Oluşturulma tarihi
    updated_at = models.DateTimeField(auto_now=True)  # Güncellenme tarihi

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    def has_module_perms(self, app_label):
        return True

    def has_perm(self, perm, obj=None):
        return True

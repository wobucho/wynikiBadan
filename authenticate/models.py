from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import PermissionsMixin, BaseUserManager, AbstractUser
from django.utils.translation import gettext_lazy as _
import jwt
from django.utils import timezone
from datetime import datetime, timedelta

from django.conf import settings

# Create your models here.

class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('type', 'ADMIN')

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)

    objects = UserManager()

    class Types(models.TextChoices):
        LEKARZ = "LEKARZ", "lekarz"
        PACJENT = "PACJENT", "pacjent"
        DIAGNOSTA = "DIAGNOSTA", "diagnosta"
        ADMIN = "ADMIN", "admin"

    type = models.CharField(_('Type'), max_length=40, choices=Types.choices, default=Types.PACJENT)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    @property
    def token(self):
        token = jwt.encode({'email': self.email, 'type': self.type, 'exp': datetime.utcnow() + timedelta(hours=1)}
                           , settings.SECRET_KEY, algorithm='HS256')
        return token


class LekarzManager(UserManager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(type=User.Types.LEKARZ)

class PacjentManager(UserManager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(type=User.Types.PACJENT)

class DiagnostaManager(UserManager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(type=User.Types.DIAGNOSTA)

class Lekarz(User):
    objects = LekarzManager()

    class Meta:
        proxy = True

    def save(self, *args, **kwargs):
        if not self.pk:
            self.type = User.Types.LEKARZ
        return super().save(*args, **kwargs)


class Pacjent(User):
    objects = PacjentManager()

    class Meta:
        proxy = True

    def save(self, *args, **kwargs):
        if not self.pk:
            self.type = User.Types.PACJENT
        return super().save(*args, **kwargs)

class Diagnosta(User):
    objects = DiagnostaManager()

    class Meta:
        proxy = True

    def save(self, *args, **kwargs):
        if not self.pk:
            self.type = User.Types.DIAGNOSTA
        return super().save(*args, **kwargs)


class PacjentProfil(models.Model):
    user = models.OneToOneField(Pacjent, on_delete=models.CASCADE, primary_key=True, related_name='profilP')
    pesel = models.CharField(max_length=11, unique=True)
    imie = models.CharField(max_length=30)
    nazwisko = models.CharField(max_length=60)
    telefon = PhoneNumberField(blank=True)

    def __str__(self):
        return f'{self.imie} {self.nazwisko} {self.pesel}'

class LekarzProfil(models.Model):
    user = models.OneToOneField(Lekarz, on_delete=models.CASCADE, primary_key=True, related_name='profilL')
    pwz = models.CharField(max_length=7, unique=True)
    imie = models.CharField(max_length=30)
    nazwisko = models.CharField(max_length=60)
    telefon = PhoneNumberField(blank=True)
    pacjenci = models.ManyToManyField(PacjentProfil, blank=True)

    def __str__(self):
        return f'{self.imie} {self.nazwisko} {self.pwz}'

class DiagnostaProfil(models.Model):
    user = models.OneToOneField(Diagnosta, on_delete=models.CASCADE, primary_key=True, related_name='profilD')
    imie = models.CharField(max_length=30)
    nazwisko = models.CharField(max_length=60)
    telefon = PhoneNumberField(blank=True)

    def __str__(self):
        return f'{self.imie} {self.nazwisko}'
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import PermissionsMixin, BaseUserManager, AbstractUser
from django.utils.translation import gettext_lazy as _
import jwt
from django.utils import timezone
from datetime import datetime, timedelta
from authenticate.models import PacjentProfil

from django.conf import settings

# Create your models here.


class badania(models.Model):
    MORFOLOGIAKRWI = 'MK'
    PROBYWATROBOWE = 'PW'
    TYPY_BADAN = [
        (MORFOLOGIAKRWI, 'Morfologia krwi'),
        (PROBYWATROBOWE, 'Próby wątrobowe'),
    ]
    pacjent = models.ForeignKey(PacjentProfil, on_delete=models.CASCADE)
    dataBadania = models.DateField(auto_now=False, auto_now_add=False)
    typBadania = models.CharField(max_length=2, choices=TYPY_BADAN, default=MORFOLOGIAKRWI)

    def __str__(self):
        return f'{self.pacjent} {self.dataBadania} {self.typBadania}'


class morfologiaKrwi(models.Model):
    badanie = models.OneToOneField(badania, on_delete=models.CASCADE, primary_key=True)
    HGB = models.DecimalField(max_digits=5, decimal_places=2, blank=True)
    HCT = models.DecimalField(max_digits=4, decimal_places=2, blank=True)
    WBC = models.DecimalField(max_digits=5, decimal_places=0, blank=True)
    RBC = models.DecimalField(max_digits=4, decimal_places=2, blank=True)
    PLT = models.DecimalField(max_digits=5, decimal_places=2, blank=True)
    CRP = models.DecimalField(max_digits=4, decimal_places=2, blank=True)

    def __str__(self):
        return f'{self.badanie}'


class probyWatrobowe(models.Model):
    badanie = models.OneToOneField(badania, on_delete=models.CASCADE, primary_key=True)
    ALT = models.DecimalField(max_digits=5, decimal_places=2, blank=True)
    AST = models.DecimalField(max_digits=5, decimal_places=2, blank=True)
    ALP = models.DecimalField(max_digits=5, decimal_places=2, blank=True)
    BIL = models.DecimalField(max_digits=5, decimal_places=2, blank=True)
    GGTP = models.DecimalField(max_digits=5, decimal_places=2, blank=True)

    def __str__(self):
        return f'{self.badanie}'
import django.contrib.auth.models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.db import models
from django.contrib.auth.models import Group, Permission, AbstractUser
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType


class LavanderiaUser(AbstractUser):
    matricula = models.CharField(max_length=64)
    apartamento = models.CharField(max_length=64)
    telefone_validator = RegexValidator(regex=r'\d{9,15}', message="São aceitos somente dígitos. De 9 a 10 caracteres")
    telefone = models.CharField(validators=[telefone_validator], max_length=64)


class Washer(models.Model):
    name = models.CharField(max_length=128, null=False)


class AvaibleSlot(models.Model):
    start = models.DateTimeField(null=False)
    washer = models.ForeignKey(Washer, on_delete=models.CASCADE, null=False)

    duration = models.DateTimeField(null=False)


class ReservedSlot(models.Model):
    slot = models.ForeignKey(AvaibleSlot, on_delete=models.CASCADE, null=False)
    user = models.ForeignKey(LavanderiaUser, on_delete=models.CASCADE, null=False)
    presence = models.BooleanField(null=False, default=True)

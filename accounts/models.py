from django.db import models
from django.contrib.auth.models import AbstractUser

import uuid


# Create your models here.


class User(AbstractUser):

    PATIENT = 'Patient'
    DOCTOR = 'Doctor'
    ROLES = [
        (PATIENT, PATIENT),
        (DOCTOR, DOCTOR),
    ]

    code = models.UUIDField(verbose_name='UserCode', primary_key=True, default=uuid.uuid4)
    application_role = models.CharField(max_length=15, verbose_name='UserRole', choices=ROLES, null=False, default=PATIENT)


class Doctor(models.Model):
    user = models.OneToOneField(User, models.CASCADE, primary_key=True)
    city = models.CharField(max_length=20, verbose_name='City', null=False)
    province = models.CharField(max_length=20, verbose_name='Province', null=False)
    region = models.CharField(max_length=20, verbose_name='Region', null=False)
    doctor_type = models.CharField(max_length=30, verbose_name='DoctorType', null=False)


class Patient(models.Model):
    user = models.OneToOneField(User, models.CASCADE, primary_key=True)
    city = models.CharField(max_length=20, verbose_name='City', null=False)
    province = models.CharField(max_length=20, verbose_name='Province', null=False)
    region = models.CharField(max_length=20, verbose_name='Region', null=False)
    doctors = models.ManyToManyField(Doctor)

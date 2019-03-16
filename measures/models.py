from django.db import models

import uuid

from accounts.models import Patient

# Create your models here.


class Parameter(models.Model):
    code = models.UUIDField(verbose_name='ParameterCode', primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=25, verbose_name='ParameterName', null=False)
    unity_measure = models.CharField(max_length=10, verbose_name='UnityMeasure')
    patient = models.ForeignKey(Patient, models.CASCADE)


class Measure(models.Model):
    code = models.UUIDField(verbose_name='MeasureCode', primary_key=True, default=uuid.uuid4, editable=False)
    value = models.FloatField(verbose_name='Value', null=False)
    date = models.DateField(verbose_name='Date', null=False)
    hour = models.CharField(verbose_name='Hour', max_length=25, null=False)
    parameter = models.ForeignKey(Parameter, models.CASCADE)

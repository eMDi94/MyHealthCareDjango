import uuid

from django.db import models

from accounts.models import Patient, Doctor

# Create your models here.


class Medicine(models.Model):

    code = models.UUIDField(verbose_name='MedicineCode', primary_key=True, default=uuid.uuid4)
    name = models.CharField(verbose_name='MedicineName', null=False, max_length=50)
    quantity = models.PositiveIntegerField(verbose_name='MedicineQuantity', null=False)
    unity = models.CharField(max_length=5, null=False)
    patient = models.ForeignKey(Patient, models.CASCADE)

    class Meta:
        unique_together = ('patient', 'name', 'quantity', 'unity',)


class Posology(models.Model):

    DAYS_OF_THE_WEEK = {
        'Monday': 'Monday',
        'Tuesday': 'Tuesday',
        'Wednesday': 'Wednesday',
        'Thursday': 'Thursday',
        'Friday': 'Friday',
        'Saturday': 'Saturday',
        'Sunday': 'Sunday',
    }

    code = models.UUIDField(verbose_name='PosologyCode', primary_key=True, default=uuid.uuid4)
    medicine = models.ForeignKey(Medicine, models.CASCADE)
    doctor = models.ForeignKey(Doctor, models.CASCADE)
    day_of_the_week = models.CharField(max_length=25, verbose_name='DayOfTheWeek')
    hour = models.CharField(max_length=25, verbose_name='Hour')
    quantity = models.CharField(max_length=25, verbose_name='Quantity')

    class Meta:
        unique_together = ('medicine', 'day_of_the_week', 'hour',)

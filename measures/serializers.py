from django.db.models import Q
from rest_framework import serializers

from .models import Parameter, Measure


class ParameterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parameter
        fields = '__all__'
        read_only_fields = ('code', 'patient',)


class MeasureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Measure
        fields = '__all__'
        read_only_fields = ('code',)

    def validate_parameter(self, value):
        # Since MeasureSerializer is used only when Measures and the only one is the patient, i can assume that request.user
        # will contain a patient
        request = self.context['request']
        user = request.user
        if value.patient.user.code != user.user.code:
            raise serializers.ValidationError()
        return value

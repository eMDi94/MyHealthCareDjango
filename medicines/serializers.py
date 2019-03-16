from rest_framework import serializers

from .models import Medicine, Posology


class MedicineSerializer(serializers.ModelSerializer):

    class Meta:
        model = Medicine
        fields = '__all__'
        read_only_fields = ('code', 'patient',)


class PosologySerializer(serializers.ModelSerializer):

    medicine = serializers.CharField(required=True, source='medicine.name')

    class Meta:
        model = Posology
        fields = '__all__'
        read_only_fields = ('code', 'doctor',)


    def create(self, validated_data):
        medicine_dict = validated_data.pop('medicine')
        p = Posology.objects.create(**validated_data, medicine_id=medicine_dict.pop('name'))
        return p

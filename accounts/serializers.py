from rest_framework import serializers, exceptions
from django.contrib.auth import authenticate
from django.db.models import Q

from .models import User, Patient, Doctor


class PatientSerializer(serializers.ModelSerializer):

    code = serializers.UUIDField(read_only=True, source='user.code')
    email = serializers.EmailField(source='user.email')
    password = serializers.CharField(write_only=True, source='user.password')
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')
    role = serializers.CharField(source='user.application_role', read_only=True)

    class Meta:
        model = Patient
        fields = ('code', 'email', 'password', 'first_name', 'last_name', 'city', 'province', 'region', 'role',)

    def create(self, validated_data):
        user_dict = validated_data.pop('user')
        user = User.objects.create_user(user_dict.get('email'), user_dict.pop('email'),
                                        password=user_dict.pop('password'), **user_dict)
        pt = Patient.objects.create(user=user, **validated_data)
        return pt


class DoctorSerializer(serializers.ModelSerializer):

    code = serializers.UUIDField(read_only=True, source='user.code')
    email = serializers.EmailField(source='user.email')
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')
    role = serializers.CharField(source='user.application_role')

    class Meta:
        model = Doctor
        fields = ('code', 'email', 'first_name', 'last_name', 'city', 'province', 'region', 'role', 'doctor_type',)
        read_only_fields = fields


class LoginSerializer(serializers.Serializer):

    LOGIN_TYPES = [
        ('PatientLogin', 'PatientLogin'),
        ('DoctorLogin', 'DoctorLogin'),
    ]

    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)
    login_type = serializers.ChoiceField(required=True, choices=LOGIN_TYPES)

    def validate(self, data):
        user = authenticate(username=data['email'], password=data['password'])
        if not user:
            raise exceptions.PermissionDenied('Invalid Input')
        required_role = User.PATIENT if data['login_type'] == 'PatientLogin' else User.DOCTOR
        if required_role != user.application_role:
            raise serializers.PermissionDenied('Invalid Input')
        if user.application_role == User.PATIENT:
            user = Patient.objects.get(user=user)
        else:
            user = Doctor.objects.get(user=user)
        return user


class PatientsDoctorsSerializer(serializers.Serializer):
    doctor_code = serializers.CharField()

    def __init__(self, instance, data, **kwargs):
        super(PatientsDoctorsSerializer, self).__init__(instance, data, **kwargs)
        self.doc = None

    def validate_doctor_code(self, value):
        qs = Doctor.objects.filter(user__code=value)
        if qs.exists():
            self.doc = qs.first()
            return value
        raise serializers.ValidationError('Invalid doctor code')

    def save(self, **kwargs):
        patient = kwargs.get('patient')
        patient.doctors.add(self.doc)
        return self.doc

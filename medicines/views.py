from django.db.models import Q
from rest_framework import generics, exceptions

from .models import Medicine, Posology
from .serializers import MedicineSerializer, PosologySerializer

from accounts.permissions import IsPatient, IsDoctor, IsAuthenticated
from accounts.models import User

import uuid

# Create your views here.


class CreateMedicineView(generics.CreateAPIView):
    serializer_class = MedicineSerializer
    permission_classes = (IsAuthenticated, IsPatient,)

    def get_queryset(self):
        return Medicine.objects.filter(patient=self.request.user)

    def perform_create(self, serializer):
        serializer.save(patient=self.request.user)


class DeleteMedicineView(generics.DestroyAPIView):
    serializer_class = MedicineSerializer
    permission_classes = (IsAuthenticated, IsPatient,)
    lookup_field = 'code'
    lookup_url_kwarg = 'medicine_code'

    def get_queryset(self):
        code = self.kwargs['medicine_code']
        qs = Medicine.objects.filter(
            Q(patient=self.request.user) & Q(code__exact=code)
        )
        if not qs.exists():
            raise exceptions.PermissionDenied('You cannot delete this medicine')
        return qs


class MedicineListView(generics.ListAPIView):
    serializer_class = MedicineSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        patient_code = self.kwargs['patient_code']
        if user.user.application_role == User.PATIENT:
            if user.user_id != uuid.UUID(patient_code):
                raise exceptions.PermissionDenied('You are not allowed')
        else:
            if not user.patient_set.filter(user_id=patient_code).exists():
                raise exceptions.PermissionDenied('You are not allowed')
        return Medicine.objects.filter(patient__user_id=patient_code)


class CreatePosologyView(generics.CreateAPIView):
    serializer_class = PosologySerializer
    permission_classes = (IsAuthenticated, IsDoctor,)

    def get_queryset(self):
        return Posology.objects.filter(doctor=self.request.user)

    def perform_create(self, serializer):
        serializer.save(doctor=self.request.user)


class DeletePosologyView(generics.DestroyAPIView):
    serializer_class = PosologySerializer
    permission_classes = (IsAuthenticated, IsDoctor,)
    lookup_field = 'code'
    lookup_url_kwarg = 'posology_code'

    def get_queryset(self):
        posology_code = self.kwargs['posology_code']
        qs = Posology.objects.filter(
            Q(doctor=self.request.user) & Q(code__exact=posology_code)
        )
        if not qs.exists():
            raise exceptions.PermissionDenied('You are not allowed to delete this posology')
        return qs


class PosologyListView(generics.ListAPIView):
    serializer_class = PosologySerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        patient_code = self.kwargs['patient_code']
        user = self.request.user
        if user.user.application_role == User.PATIENT:
            if user.user_id != uuid.UUID(patient_code):
                raise exceptions.PermissionDenied('You cannot access this data')
        else:
            if not user.patient_set.filter(user_id=patient_code).exists():
                raise exceptions.PermissionDenied('You cannot access this data')
        return Posology.objects.filter(medicine__patient__user_id=patient_code)

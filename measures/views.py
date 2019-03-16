from django.db.models import Q
from rest_framework import generics, exceptions

from .models import Measure, Parameter
from .serializers import MeasureSerializer, ParameterSerializer

from accounts.models import User
from accounts.permissions import IsPatient, IsAuthenticated

import uuid

# Create your views here.


class CreateParameterView(generics.CreateAPIView):
    serializer_class = ParameterSerializer
    permission_classes = (IsAuthenticated, IsPatient,)

    def get_queryset(self):
        return Parameter.objects.filter(patient=self.request.user)

    def perform_create(self, serializer):
        serializer.save(patient=self.request.user)


class DeleteParameterView(generics.DestroyAPIView):
    serializer_class = ParameterSerializer
    permission_classes = (IsAuthenticated, IsPatient,)
    lookup_field = 'code'
    lookup_url_kwarg = 'parameter_code'

    def get_queryset(self):
        parameter_code = self.kwargs['parameter_code']
        qs = Parameter.objects.filter(
            Q(patient_id=self.request.user.user.code) & Q(code=parameter_code)
        )
        if not qs.exists():
            raise exceptions.ValidationError
        return qs


class ParameterListView(generics.ListAPIView):
    serializer_class = ParameterSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        if user.user.application_role == User.PATIENT:
            qs = Parameter.objects.filter(patient_id=user.user.code)
        else:
            qs = Parameter.objects.filter(patient__in=user.patient_set.all())
        patient_code = self.kwargs['patient_code']
        qs = qs.filter(patient_id=uuid.UUID(patient_code))
        return qs


class CreateMeasureView(generics.CreateAPIView):
    serializer_class = MeasureSerializer
    permission_classes = (IsAuthenticated, IsPatient,)

    def get_queryset(self):
        return Measure.objects.filter(parameter__patient_id=self.request.user.user.code)


class DeleteMeasureView(generics.DestroyAPIView):
    serializer_class = MeasureSerializer
    permission_classes = (IsAuthenticated, IsPatient,)
    lookup_field = 'code'
    lookup_url_kwarg = 'measure_code'

    def get_queryset(self):
        return Measure.objects.filter(parameter__patient_id=self.request.user.id)


class RangeMeasureListView(generics.ListAPIView):
    serializer_class = MeasureSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        patient_code = self.kwargs['patient_code']
        if user.user.application_role == User.PATIENT:
            if user.user.code != uuid.UUID(patient_code):
                raise exceptions.PermissionDenied
        else:
            try:
                user.patient_set.get(user__code=patient_code)
            except User.DoesNotExist:
                raise exceptions.PermissionDenied
        query = self.request.query_params
        start, end = query.get('start'), query.get('end')
        if not start or not end:
            raise exceptions.ValidationError
        return Measure.objects.filter(
            Q(parameter__patient_id=patient_code) & Q(date__range=(start, end))
        )

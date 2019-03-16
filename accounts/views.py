from django.db.models import Q

from rest_framework import generics, exceptions, views, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes

from .models import User, Patient, Doctor
from .serializers import PatientSerializer, DoctorSerializer, PatientsDoctorsSerializer, LoginSerializer
from .permissions import IsPatient, IsDoctor, IsAuthenticated
from .auth import CustomTokenAuthentication

from knox.models import AuthToken

import json

# Create your views here.


class PatientRegistrationView(generics.GenericAPIView):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            'user': PatientSerializer(user, context=self.get_serializer_context()).data,
            'token': AuthToken.objects.create(user=user.user)
        }, status.HTTP_201_CREATED)


class LoginView(generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except exceptions.PermissionDenied:
            return Response(data={'message': 'Invalid Credentials'}, status=401)
        user = serializer.validated_data
        if user.user.application_role == User.PATIENT:
            out_ser = PatientSerializer
        else:
            out_ser = DoctorSerializer
        return Response({
            'user': out_ser(user, context=self.get_serializer_context()).data,
            'token': AuthToken.objects.create(user=user.user)
        }, status.HTTP_200_OK)


class LogoutView(views.APIView):

    def post(self, request, *args, **kwargs):
        request._auth.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class LogoutAllView(views.APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        request.user.user.auth_token_set.all().delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class RetrieveUserInformation(generics.RetrieveAPIView):
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        user = self.request.user
        if user.user.application_role == User.PATIENT:
            return PatientSerializer
        else:
            return DoctorSerializer

    def get_object(self):
        return self.request.user


class SearchDoctorListView(generics.ListAPIView):
    serializer_class = DoctorSerializer
    permission_classes = (IsAuthenticated, IsPatient,)

    def get_queryset(self):
        query_params = self.request.query_params
        first_name, last_name = query_params.get('first-name'), query_params.get('last-name')
        return Doctor.objects.filter(
            Q(user__first_name__exact=first_name) & Q(user__last_name__exact=last_name) &
            Q(user__application_role__exact=User.DOCTOR)
        )


class MyPatientsListView(generics.ListAPIView):
    serializer_class = PatientSerializer
    permission_classes = (IsAuthenticated, IsDoctor,)

    def get_queryset(self):
        user = self.request.user
        return user.patient_set


class MyDoctorsListView(generics.ListAPIView):
    serializer_class = DoctorSerializer
    permission_classes = (IsAuthenticated, IsPatient,)

    def get_queryset(self):
        return self.request.user.doctors


@api_view(['POST'])
@permission_classes([IsAuthenticated, IsPatient])
def add_doctor(request):
    serializer = PatientsDoctorsSerializer(instance=None, data=json.loads(request.body))
    serializer.is_valid(raise_exception=True)
    instance = serializer.save(patient=request.user)
    return Response(DoctorSerializer(instance).data, 201)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated, IsPatient])
def delete_doctor(request, *args, **kwargs):
    serializer = PatientsDoctorsSerializer(instance=None, data=kwargs)
    serializer.is_valid(raise_exception=True)
    doc = serializer.doc
    request.user.doctors.remove(doc)
    return Response(status=204)

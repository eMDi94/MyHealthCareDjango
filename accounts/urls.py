from django.urls import path

from .views import (PatientRegistrationView, LoginView, delete_doctor, add_doctor, RetrieveUserInformation,
                    SearchDoctorListView, MyDoctorsListView, MyPatientsListView, LogoutView, LogoutAllView)



urlpatterns = [
    path('patient/patient-registration/', PatientRegistrationView.as_view()),
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('logout-all', LogoutAllView.as_view()),
    path('retrieve-user/', RetrieveUserInformation.as_view()),
    path('patient/search-doctors/', SearchDoctorListView.as_view()),
    path('patient/my-doctors/', MyDoctorsListView.as_view()),
    path('doctor/my-patients/', MyPatientsListView.as_view()),
    path('patient/add-doctor/', add_doctor),
    path('patient/delete-doctor/', delete_doctor)
]

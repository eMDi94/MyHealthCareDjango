from django.urls import path

from .views import (CreatePosologyView, CreateMedicineView, DeletePosologyView, DeleteMedicineView,
                    MedicineListView, PosologyListView)


urlpatterns = [
    path('patient/create-medicine/', CreateMedicineView.as_view()),
    path('patient/delete-medicine/<str:medicine_code>/', DeleteMedicineView.as_view()),
    path('<str:patient_code>/', MedicineListView.as_view()),
    path('doctor/create-posology/', CreatePosologyView.as_view()),
    path('doctor/delete-posology/<str:posology_code>/', DeletePosologyView.as_view()),
    path('posologies/<str:patient_code>/', PosologyListView.as_view()),
]

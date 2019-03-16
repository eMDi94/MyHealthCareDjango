from django.urls import path

from .views import (CreateMeasureView, CreateParameterView, DeleteMeasureView, DeleteParameterView,
                    RangeMeasureListView, ParameterListView)


urlpatterns = [
    path('patient/create-parameter/', CreateParameterView.as_view()),
    path('patient/delete-parameter/<str:parameter_code>/', DeleteParameterView.as_view()),
    path('parameters/<str:patient_code>/', ParameterListView.as_view()),
    path('patient/create-measure/', CreateMeasureView.as_view()),
    path('patient/delete-measure/<str:measure_code>', DeleteMeasureView.as_view()),
    path('<str:patient_code>/', RangeMeasureListView.as_view()),
]

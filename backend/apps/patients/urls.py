from django.urls import path

from apps.patients.views import PatientDetailView, PatientListView

urlpatterns = [
    path("patients", PatientListView.as_view()),
    path("patients/<str:mrn>", PatientDetailView.as_view()),
]

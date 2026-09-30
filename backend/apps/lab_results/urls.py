from django.urls import path

from apps.lab_results.views import LabImportJobDetailView, LabImportUploadView

urlpatterns = [
    path("lab-imports", LabImportUploadView.as_view()),
    path("lab-imports/<int:pk>", LabImportJobDetailView.as_view()),
]

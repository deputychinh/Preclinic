from django.urls import path

from apps.encounters.views import EncounterDetailView, EncounterListCreateView, SignNoteView

urlpatterns = [
    path("encounters", EncounterListCreateView.as_view()),
    path("encounters/<int:pk>", EncounterDetailView.as_view()),
    path("encounters/<int:pk>/sign", SignNoteView.as_view()),
]

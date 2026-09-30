from django.urls import path

from apps.ai_assistant.views import AIDraftApproveView, AIDraftDetailView, AIDraftRequestView

urlpatterns = [
    path("encounters/<int:encounter_id>/ai-drafts", AIDraftRequestView.as_view()),
    path("ai-drafts/<int:pk>", AIDraftDetailView.as_view()),
    path("ai-drafts/<int:pk>/approve", AIDraftApproveView.as_view()),
]

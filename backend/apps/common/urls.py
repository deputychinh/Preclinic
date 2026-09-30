from django.urls import path

from apps.common.views import DashboardSummaryView, HealthView

urlpatterns = [
    path("health", HealthView.as_view()),
    path("dashboard/summary", DashboardSummaryView.as_view()),
]

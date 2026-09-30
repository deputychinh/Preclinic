from django.urls import path

from apps.care_plans.views import CarePlanDetailView, CarePlanListCreateView

urlpatterns = [
    path("care-plans", CarePlanListCreateView.as_view()),
    path("care-plans/<int:pk>", CarePlanDetailView.as_view()),
]

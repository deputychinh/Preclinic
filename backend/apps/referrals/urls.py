from django.urls import path

from apps.referrals.views import ReferralListCreateView

urlpatterns = [path("referrals", ReferralListCreateView.as_view())]

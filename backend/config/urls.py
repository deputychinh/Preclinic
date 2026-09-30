from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path("api/v1/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/v1/schema/swagger-ui/", SpectacularSwaggerView.as_view(url_name="schema")),
    path("api/v1/", include("apps.common.urls")),
    path("api/v1/auth/", include("apps.accounts.urls")),
    path("api/v1/", include("apps.patients.urls")),
    path("api/v1/", include("apps.encounters.urls")),
    path("api/v1/", include("apps.care_plans.urls")),
    path("api/v1/", include("apps.referrals.urls")),
    path("api/v1/", include("apps.lab_results.urls")),
    path("api/v1/", include("apps.audit.urls")),
    path("api/v1/", include("apps.ai_assistant.urls")),
]

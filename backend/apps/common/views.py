from typing import cast

from django.conf import settings
from django.db import connections
from django.db.utils import OperationalError
from redis import Redis
from redis.exceptions import RedisError
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.accounts.models import User
from apps.common.dashboard import get_dashboard_summary


class HealthView(APIView):
    """Liveness + dependency check for the load balancer. No auth required."""

    permission_classes = [AllowAny]

    def get(self, request):  # type: ignore[no-untyped-def]
        db_ok = self._check_db()
        redis_ok = self._check_redis()
        healthy = db_ok and redis_ok
        return Response(
            {"status": "ok" if healthy else "degraded", "database": _ok(db_ok), "redis": _ok(redis_ok)},
            status=200 if healthy else 503,
        )

    @staticmethod
    def _check_db() -> bool:
        try:
            connections["default"].cursor().execute("SELECT 1")
            return True
        except OperationalError:
            return False

    @staticmethod
    def _check_redis() -> bool:
        try:
            Redis.from_url(getattr(settings, "REDIS_URL", "redis://localhost:6379/0")).ping()
            return True
        except RedisError:
            return False


def _ok(value: bool) -> str:
    return "ok" if value else "down"


class DashboardSummaryView(APIView):
    """Role-aware landing-page summary: stat counts + recent activity (added post-build for a
    real dashboard instead of redirecting straight to /patients)."""

    def get(self, request):  # type: ignore[no-untyped-def]
        user = cast(User, request.user)
        return Response(get_dashboard_summary(user=user))

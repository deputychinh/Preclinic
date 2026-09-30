"""Role-aware landing-page summary (F1-adjacent, not in the original FR list — added post-build
per user request for a real dashboard instead of a redirect straight to /patients).

Deliberately its own module, not apps/common/selectors.py: it reads across five domain apps
(patients, encounters, referrals, ai_assistant, audit), which none of those apps' own
selectors.py files should import from each other to do — this is the one place that's allowed
to aggregate across app boundaries."""

from datetime import timedelta
from typing import Any

from django.db.models import Count
from django.utils import timezone

from apps.accounts.models import User
from apps.ai_assistant.models import AIDraft
from apps.audit.models import AuditEvent
from apps.common.enums import AIDraftStatus, ReferralStatus, Role
from apps.encounters.models import Encounter
from apps.patients.models import Patient
from apps.referrals.models import Referral


def get_dashboard_summary(*, user: User) -> dict[str, Any]:
    if user.role == Role.COMPLIANCE_OFFICER:
        return _compliance_summary(user)
    return _clinical_summary(user)


def _clinical_summary(user: User) -> dict[str, Any]:
    patients = Patient.objects.for_user(user).alive()
    week_ago = timezone.now() - timedelta(days=7)

    patient_count = patients.count()
    encounters_this_week = Encounter.objects.filter(
        patient__in=patients, occurred_at__gte=week_ago
    ).count()
    pending_ai_drafts = AIDraft.objects.filter(
        encounter__patient__in=patients,
        status__in=[AIDraftStatus.PENDING, AIDraftStatus.READY],
    ).count()
    open_referrals = Referral.objects.filter(
        patient__in=patients, status=ReferralStatus.REQUESTED
    ).count()

    recent_events = list(
        AuditEvent.objects.filter(actor=user)
        .select_related("actor")
        .order_by("-created_at")[:5]
        .values("id", "action", "resource_type", "patient_id", "is_break_glass", "created_at")
    )

    referral_breakdown = _counts_by(Referral.objects.filter(patient__in=patients), "status")
    encounter_breakdown = _counts_by(Encounter.objects.filter(patient__in=patients), "status")

    return {
        "role": user.role,
        "patient_count": patient_count,
        "encounters_this_week": encounters_this_week,
        "pending_ai_drafts": pending_ai_drafts,
        "open_referrals": open_referrals,
        "recent_events": recent_events,
        "referral_breakdown": referral_breakdown,
        "encounter_breakdown": encounter_breakdown,
    }


def _compliance_summary(user: User) -> dict[str, Any]:
    today_start = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
    week_ago = timezone.now() - timedelta(days=7)

    events_today = AuditEvent.objects.filter(created_at__gte=today_start).count()
    break_glass_this_week = AuditEvent.objects.filter(
        is_break_glass=True, created_at__gte=week_ago
    ).count()
    total_events_this_week = AuditEvent.objects.filter(created_at__gte=week_ago).count()

    recent_events = list(
        AuditEvent.objects.select_related("actor")
        .order_by("-created_at")[:5]
        .values("id", "action", "resource_type", "patient_id", "is_break_glass", "created_at")
    )

    action_breakdown = _counts_by(AuditEvent.objects.filter(created_at__gte=week_ago), "action")

    return {
        "role": user.role,
        "events_today": events_today,
        "break_glass_this_week": break_glass_this_week,
        "total_events_this_week": total_events_this_week,
        "recent_events": recent_events,
        "action_breakdown": action_breakdown,
    }


def _counts_by(queryset: Any, field: str) -> list[dict[str, Any]]:
    """[{"label": <value>, "count": <n>}, ...] — the flat shape the frontend chart consumes."""
    rows = queryset.values(field).annotate(count=Count("id")).order_by("-count")
    return [{"label": row[field], "count": row["count"]} for row in rows]

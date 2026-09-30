"""Shared abstract base models: timestamps and soft delete + legal hold (DS-11, NFR-01/12)."""

from typing import Self

from django.db import models
from django.utils import timezone


class TimestampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class SoftDeleteQuerySet(models.QuerySet):
    def alive(self) -> Self:
        return self.filter(deleted_at__isnull=True)


class SoftDeleteModel(models.Model):
    """No hard DELETE on clinical/audit tables. `legal_hold` blocks deletion entirely, even soft."""

    deleted_at = models.DateTimeField(null=True, blank=True)
    legal_hold = models.BooleanField(default=False)

    objects = SoftDeleteQuerySet.as_manager()

    class Meta:
        abstract = True

    def soft_delete(self) -> None:
        if self.legal_hold:
            raise ValueError("Cannot delete a record under legal hold")
        self.deleted_at = timezone.now()
        self.save(update_fields=["deleted_at"])

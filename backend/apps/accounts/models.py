from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models

from apps.accounts.managers import UserManager
from apps.common.enums import Role
from apps.common.models import TimestampedModel


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    role = models.CharField(max_length=32, choices=Role.choices)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name", "role"]

    class Meta:
        ordering = ["last_name", "first_name"]

    def __str__(self) -> str:
        return f"{self.get_full_name()} ({self.role})"

    def get_full_name(self) -> str:
        return f"{self.first_name} {self.last_name}".strip()


class CareTeam(TimestampedModel):
    """A named group of clinicians/coordinators who share access to a set of patients."""

    name = models.CharField(max_length=150, unique=True)

    def __str__(self) -> str:
        return self.name


class CareTeamMembership(TimestampedModel):
    care_team = models.ForeignKey(CareTeam, on_delete=models.CASCADE, related_name="memberships")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="care_team_memberships")

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["care_team", "user"], name="uq_care_team_membership"),
        ]

    def __str__(self) -> str:
        return f"{self.user} @ {self.care_team}"

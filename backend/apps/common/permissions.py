"""Role-based permission classes. Care-team scoping itself lives in each app's selectors (DS-02);
these classes only gate *which role* may call an endpoint at all."""

from rest_framework.permissions import BasePermission

from apps.common.enums import Role


class HasRole(BasePermission):
    """Usage: `permission_classes = [HasRole.for_roles(Role.CLINICIAN)]`."""

    allowed_roles: tuple[Role, ...] = ()

    def has_permission(self, request, view) -> bool:  # type: ignore[no-untyped-def]
        user = request.user
        return bool(user and user.is_authenticated and user.role in self.allowed_roles)

    @classmethod
    def for_roles(cls, *roles: Role) -> type["HasRole"]:
        return type(f"HasRole_{'_'.join(roles)}", (cls,), {"allowed_roles": roles})


IsClinician = HasRole.for_roles(Role.CLINICIAN)
IsCareCoordinator = HasRole.for_roles(Role.CARE_COORDINATOR)
IsComplianceOfficer = HasRole.for_roles(Role.COMPLIANCE_OFFICER)
IsClinicianOrCoordinator = HasRole.for_roles(Role.CLINICIAN, Role.CARE_COORDINATOR)

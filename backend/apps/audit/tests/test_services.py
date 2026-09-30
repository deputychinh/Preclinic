import pytest
from django.db import transaction

from apps.audit.services import record_access
from apps.common.enums import AuditAction
from apps.common.tests.factories import UserFactory

pytestmark = pytest.mark.django_db


@pytest.mark.django_db(transaction=True)
def test_record_access_requires_an_open_transaction():
    """DS-04: calling this outside an atomic block is a programming error, not a soft failure —
    it must raise loudly so a missing transaction is caught in development, not in production.
    Needs transaction=True: the default `django_db` fixture wraps every test in its own outer
    transaction, which would make `in_atomic_block` true even here and hide this exact bug."""
    actor = UserFactory()

    with pytest.raises(AssertionError):
        record_access(actor=actor, action=AuditAction.READ, resource_type="Patient", resource_id="1")


def test_record_access_succeeds_inside_atomic_block():
    actor = UserFactory()

    with transaction.atomic():
        event = record_access(actor=actor, action=AuditAction.READ, resource_type="Patient", resource_id="1")

    assert event.id is not None

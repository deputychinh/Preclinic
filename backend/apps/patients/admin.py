from django.contrib import admin

from apps.patients.models import Allergy, Consent, Medication, Patient

admin.site.register(Patient)
admin.site.register(Allergy)
admin.site.register(Medication)
admin.site.register(Consent)

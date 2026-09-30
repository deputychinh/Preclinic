from django.contrib import admin

from apps.encounters.models import DiagnosisCode, Encounter, EncounterNoteVersion

admin.site.register(Encounter)
admin.site.register(EncounterNoteVersion)
admin.site.register(DiagnosisCode)

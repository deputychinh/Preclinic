from django.contrib import admin

from apps.lab_results.models import LabImportJob, LabResult

admin.site.register(LabResult)
admin.site.register(LabImportJob)

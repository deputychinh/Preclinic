from django.contrib import admin

from apps.care_plans.models import CarePlan, CarePlanTask

admin.site.register(CarePlan)
admin.site.register(CarePlanTask)

from django.contrib import admin

# Register your models here.
# health/admin.py
from django.contrib import admin
from .models import (
    Disease, Vaccination, VaccinationRecord, Mortality,
    WaterConsumption, HealthStatus, ChickenEnvironment,
    NutritionInformation
)

@admin.register(Disease)
class DiseaseAdmin(admin.ModelAdmin):
    list_display = ('name', 'severity', 'zoonotic', 'created_at')
    search_fields = ('name', 'scientific_name', 'description')
    list_filter = ('severity', 'zoonotic')

@admin.register(Vaccination)
class VaccinationAdmin(admin.ModelAdmin):
    list_display = ('name', 'disease', 'dosage', 'frequency', 'duration')
    search_fields = ('name', 'disease__name')
    list_filter = ('disease',)

@admin.register(VaccinationRecord)
class VaccinationRecordAdmin(admin.ModelAdmin):
    list_display = ('vaccine', 'chicken', 'date_administered', 'next_due_date', 'administered_by')
    search_fields = ('vaccine__name', 'chicken__tag_number')
    list_filter = ('vaccine', 'date_administered')

@admin.register(Mortality)
class MortalityAdmin(admin.ModelAdmin):
    list_display = ('chicken', 'date', 'reason')
    search_fields = ('chicken__tag_number', 'reason')
    list_filter = ('date',)

@admin.register(WaterConsumption)
class WaterConsumptionAdmin(admin.ModelAdmin):
    list_display = ('chicken', 'liters', 'date')
    search_fields = ('chicken__tag_number',)
    list_filter = ('date',)

@admin.register(HealthStatus)
class HealthStatusAdmin(admin.ModelAdmin):
    list_display = ('chicken', 'status', 'count', 'checkup_date')
    search_fields = ('chicken__tag_number',)
    list_filter = ('status', 'checkup_date')

@admin.register(ChickenEnvironment)
class ChickenEnvironmentAdmin(admin.ModelAdmin):
    list_display = ('temperature', 'humidity', 'cleanliness', 'stocking_density', 'recorded_at')
    list_filter = ('recorded_at',)

@admin.register(NutritionInformation)
class NutritionInformationAdmin(admin.ModelAdmin):
    list_display = ('feed_type', 'feeding_schedule', 'food_consumption_kg', 'water_consumption_ml', 'recorded_at')
    list_filter = ('recorded_at',)

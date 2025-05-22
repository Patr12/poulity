from django.shortcuts import render
# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import (
    Disease, Vaccination, VaccinationRecord,
    Mortality, WaterConsumption, HealthStatus,
    ChickenEnvironment, NutritionInformation
)
from .forms import (
    DiseaseForm, VaccinationForm, VaccinationRecordForm,
    MortalityForm, WaterConsumptionForm, HealthStatusForm,
    ChickenEnvironmentForm, NutritionInformationForm
)

# === DISEASE VIEWS ===
@login_required
def disease_list(request):
    diseases = Disease.objects.all()
    return render(request, 'health/disease_list.html', {'diseases': diseases})

@login_required
def disease_detail(request, pk):
    disease = get_object_or_404(Disease, pk=pk)
    return render(request, 'health/disease_detail.html', {'disease': disease})

# === VACCINATION VIEWS ===
@login_required
def vaccination_list(request):
    vaccines = Vaccination.objects.select_related('disease').all()
    return render(request, 'health/vaccination_list.html', {'vaccines': vaccines})

# === VACCINATION RECORD VIEWS ===
@login_required
def vaccination_records(request):
    records = VaccinationRecord.objects.select_related('chicken', 'vaccine').all()
    return render(request, 'health/vaccination_records.html', {'records': records})

# === MORTALITY VIEWS ===
@login_required
def mortality_list(request):
    mortalities = Mortality.objects.select_related('chicken').all()
    return render(request, 'health/mortality_list.html', {'mortalities': mortalities})

# === WATER CONSUMPTION ===
@login_required
def water_usage_list(request):
    usages = WaterConsumption.objects.select_related('chicken').all()
    return render(request, 'health/water_usage_list.html', {'usages': usages})

# === HEALTH STATUS CHECKS ===
@login_required
def health_status_list(request):
    checks = HealthStatus.objects.select_related('chicken').all()
    return render(request, 'health/health_status_list.html', {'checks': checks})

# === CHICKEN ENVIRONMENT ===
@login_required
def environment_logs(request):
    logs = ChickenEnvironment.objects.all().order_by('-recorded_at')
    return render(request, 'health/environment_logs.html', {'logs': logs})

# === NUTRITION INFORMATION ===
@login_required
def nutrition_logs(request):
    logs = NutritionInformation.objects.all().order_by('-recorded_at')
    return render(request, 'health/nutrition_logs.html', {'logs': logs})

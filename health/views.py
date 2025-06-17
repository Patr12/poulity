from django.shortcuts import render
# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

from core.forms import ChickenHealthStatusForm
from core.models import Chicken, Feeding
from .models import (
    Disease, Vaccination, VaccinationRecord,
    Mortality, WaterConsumption, HealthStatus,
    ChickenEnvironment, NutritionInformation
)
from .forms import (
    DiseaseForm, FeedingForm, VaccinationForm, VaccinationRecordForm,
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
    return render(request, 'healths/vaccination_list.html', {'vaccines': vaccines})

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


def add_feeding(request):
    if request.method == 'POST':
        form = FeedingForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('core:feeding')
    else:
        form = FeedingForm()
    
    return render(request, 'feeding/feeding_form.html', {'form': form})

def edit_feeding(request, pk):
    feeding = get_object_or_404(Feeding, pk=pk)
    if request.method == 'POST':
        form = FeedingForm(request.POST, instance=feeding)
        if form.is_valid():
            form.save()
            return redirect('core:feeding')
    else:
        form = FeedingForm(instance=feeding)
    
    return render(request, 'feeding/feeding_form.html', {'form': form})

def delete_feeding(request, pk):
    feeding = get_object_or_404(Feeding, pk=pk)
    if request.method == 'POST':
        feeding.delete()
        return redirect('core:feeding')
    return render(request, 'feeding/feeding_confirm_delete.html', {'feeding': feeding})

def chicken_detail(request, pk):
    chicken = get_object_or_404(Chicken, pk=pk)
    # Add any additional context you need
    return render(request, 'feeding/chicken_detail.html', {'chicken': chicken})


def add_health_status(request):
    if request.method == 'POST':
        form = ChickenHealthStatusForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('core:health_dashboard')
    else:
        form = ChickenHealthStatusForm()
    return render(request, 'healths/health_status_form.html', {'form': form})

def edit_health_status(request, pk):
    health_status = get_object_or_404(HealthStatus, pk=pk)
    if request.method == 'POST':
        form = ChickenHealthStatusForm(request.POST, instance=health_status)
        if form.is_valid():
            form.save()
            return redirect('core:health_dashboard')
    else:
        form = ChickenHealthStatusForm(instance=health_status)
    return render(request, 'chealths/health_status_form.html', {'form': form})

def delete_health_status(request, pk):
    health_status = get_object_or_404(HealthStatus, pk=pk)
    if request.method == 'POST':
        health_status.delete()
        return redirect('core:health_dashboard')
    return render(request, 'healths/health_status_confirm_delete.html', {'health_status': health_status})


from django.shortcuts import redirect, render

from .forns import ChickenEnvironmentForm, ChickenHealthStatusForm, DiseaseForm, HealthReportForm, NutritionInformationForm, SettingsForm, VaccinationRecordForm
from .models import Chicken, EggProduction, Feeding, HealthStatus, Incubation, Chick, Customer, Mortality, Order, Settings, WaterConsumption, ChickenEnvironment, Disease, VaccinationRecord, NutritionInformation, HealthReport
from django.shortcuts import render
from .utils import send_update_email
from django.utils import timezone
from django.db.models import Sum
import logging


def home(request):
    context = {
        'total_chickens': Chicken.objects.count(),
        'total_eggs': EggProduction.objects.aggregate(total=Sum('number_of_eggs'))['total'] or 0,
        'ongoing_incubations': Incubation.objects.filter(is_hatched=False).count(),
        'total_chicks': Chick.objects.aggregate(total=Sum('number_of_chicks'))['total'] or 0,
        'total_orders': Order.objects.count(),
        'total_customers': Customer.objects.count(),
        'recent_feedings': Feeding.objects.select_related('chicken').order_by('-feeding_time')[:5],
        'recent_health_checks': HealthStatus.objects.select_related('chicken').order_by('-checkup_date')[:5],
    }
    return render(request, 'core/home.html', context)


def about(request):
    return render(request, 'core/about.html')

def contact(request):
    return render(request, 'core/contact.html')

# ==== Ulishaji ====
def feeding(request):
    feedings = Feeding.objects.select_related('chicken').order_by('-feeding_time')
    return render(request, 'core/feeding.html', {'feedings': feedings})

# ==== Maagizo ya Wateja ====
def order(request):
    orders = Order.objects.select_related('customer').order_by('-order_date')
    return render(request, 'core/order.html', {'orders': orders})

# ==== Afya ya Kuku ====
def health_dashboard(request):
    if request.method == 'POST':
        health_form = ChickenHealthStatusForm(request.POST)
        disease_form = DiseaseForm(request.POST)
        vaccination_form = VaccinationRecordForm(request.POST)
        environment_form = ChickenEnvironmentForm(request.POST)
        nutrition_form = NutritionInformationForm(request.POST)
        report_form = HealthReportForm(request.POST)

        if all([
            health_form.is_valid(), disease_form.is_valid(), vaccination_form.is_valid(),
            environment_form.is_valid(), nutrition_form.is_valid(), report_form.is_valid()
        ]):
            health_form.save()
            disease_form.save()
            vaccination_form.save()
            environment_form.save()
            nutrition_form.save()
            report_form.save()
            return redirect('health_dashboard')

    else:
        health_form = ChickenHealthStatusForm()
        disease_form = DiseaseForm()
        vaccination_form = VaccinationRecordForm()
        environment_form = ChickenEnvironmentForm()
        nutrition_form = NutritionInformationForm()
        report_form = HealthReportForm()

    # Fetch data from database
    health_data = HealthStatus.objects.all()
    disease_data = Disease.objects.all()
    vaccination_data = VaccinationRecord.objects.all()
    environment_data = ChickenEnvironment.objects.all()
    nutrition_data = NutritionInformation.objects.all()
    report_data = HealthReport.objects.all()

    context = {
        'health_form': health_form,
        'disease_form': disease_form,
        'vaccination_form': vaccination_form,
        'environment_form': environment_form,
        'nutrition_form': nutrition_form,
        'report_form': report_form,
        'health_data': health_data,
        'disease_data': disease_data,
        'vaccination_data': vaccination_data,
        'environment_data': environment_data,
        'nutrition_data': nutrition_data,
        'report_data': report_data,
    }
    return render(request, 'core/health_dashboard.html', context)

def report(request):
    from_date = request.GET.get('from_date')
    to_date = request.GET.get('to_date')

    reports = []

    if from_date and to_date:
        from_date = timezone.datetime.strptime(from_date, '%Y-%m-%d').date()
        to_date = timezone.datetime.strptime(to_date, '%Y-%m-%d').date()

        egg_data = EggProduction.objects.filter(date_laid__range=(from_date, to_date))
        chick_data = Chick.objects.filter(hatch_date__range=(from_date, to_date))
        incubation_data = Incubation.objects.filter(start_date__range=(from_date, to_date))

        reports = {
            'total_eggs': egg_data.aggregate(sum('number_of_eggs'))['number_of_eggs__sum'] or 0,
            'total_chicks': chick_data.aggregate(sum('number_of_chicks'))['number_of_chicks__sum'] or 0,
            'incubations': incubation_data.count(),
        }

    return render(request, 'core/report.html', {'reports': reports})

# ==== Mipangilio ya mfumo ====
def settings(request):
    settings = Settings.objects.all()

    if request.method == 'POST':
        form = SettingsForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('settings')
    else:
        form = SettingsForm()

    return render(request, 'core/settings.html', {'settings': settings, 'form': form})

def calenda(request):
    events = []

    for incubation in Incubation.objects.all():
        events.append({
            'event': f"Incubation start for {incubation.chicken}",
            'date': incubation.start_date
        })
        events.append({
            'event': f"Expected hatch for {incubation.chicken}",
            'date': incubation.expected_hatch_date
        })

    for chick in Chick.objects.all():
        events.append({
            'event': f"{chick.number_of_chicks} chicks hatched",
            'date': chick.hatch_date
        })

    for egg in EggProduction.objects.all():
        events.append({
            'event': f"{egg.number_of_eggs} eggs laid",
            'date': egg.date_laid
        })

    return render(request, 'core/calenda.html', {'events': events})

def chicken_view(request):
    chickens = Chicken.objects.all()
    return render(request, 'core/chicken.html', {'chickens': chickens})

def egg_production_view(request):
    eggs = EggProduction.objects.all()
    return render(request, 'core/eggproduction.html', {'eggs': eggs})
#email responce for eggproduction
logger = logging.getLogger(__name__)

def egg_production_view(request):
    eggs = EggProduction.objects.all()

    for egg in eggs:
        try:
            customer = egg.chicken.customer  # Make sure this relationship exists
            message = f"Your chicken {egg.chicken.tag_number} laid {egg.number_of_eggs} eggs on {egg.date_laid}."
            send_update_email("Egg Production Update", message, customer.email)
        except Exception as e:
            # Log the error so you can track it without crashing the view
            logger.error(f"Error sending email to {customer.email if 'customer' in locals() else 'unknown'}: {e}")

    return render(request, 'core/eggproduction.html', {'eggs': eggs})

def incubation_view(request):
    incubations = Incubation.objects.all()
    return render(request, 'core/incubation.html', {'incubations': incubations})

def chick_growth_view(request):
    chicks = Chick.objects.all()
    return render(request, 'core/chick_growth.html', {'chicks': chicks})

def customer_view(request):
    customers = Customer.objects.all()
    return render(request, 'core/customer.html', {'customers': customers})

# ==== Maji yaliyotumika ====
def water_consumption_view(request):
    water_data = WaterConsumption.objects.all()
    return render(request, 'core/water_consumption.html', {'water_data': water_data})

# ==== Vifo vya kuku ====
def mortality_view(request):
    mortalities = Mortality.objects.all()
    return render(request, 'core/mortality.html', {'mortalities': mortalities})

#calenda

# login


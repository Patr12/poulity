from django.shortcuts import redirect, render
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from core.forms import (
    ChickenEnvironmentForm, ChickenHealthStatusForm, DiseaseForm, EggProductionForm, HealthReportForm,
    NutritionInformationForm, SettingsForm, VaccinationRecordForm
)
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib import messages
from django.views.generic import CreateView
from django.db.models import Sum
from django.utils import timezone
from datetime import timedelta
from core.models import Chicken, Feeding,  Order, Settings
from customers.models import Customer
from health.models import ChickenEnvironment, Disease, HealthStatus, Mortality, NutritionInformation, VaccinationRecord, WaterConsumption
from inventory.models import Chick
from production.forms import OrderForm
from production.models import EggProduction, Incubation, Product
from reports.models import HealthReport
from .utils import send_update_email
from django.utils import timezone
from django.db.models import Sum
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout
import logging

logger = logging.getLogger(__name__)

# Signup view
def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'accounts/signup.html', {'form': form})
@login_required
def profile_view(request):
    user = request.user
    # Kama unataka kuonyesha data kutoka apps zingine, itegemea user
    # Mfano, onyesha idadi ya records za afya au mayai aliyozalisha
    health_records_count = HealthStatus.objects.filter(chicken__owner=user).count()
    egg_productions_count = EggProduction.objects.filter(owner=user).count()

    context = {
        'user': user,
        'health_records_count': health_records_count,
        'egg_productions_count': egg_productions_count,
    }
    return render(request, 'profile.html', context)
# Homepage dashboard
def home(request):
    # Calculate weekly egg production
    week_ago = timezone.now() - timedelta(days=7)
    weekly_eggs = EggProduction.objects.filter(
        date_laid__gte=week_ago
    ).aggregate(total=Sum('number_of_eggs'))['total'] or 0
    
    # Set weekly target (you can make this dynamic)
    weekly_target = 100
    weekly_progress = min(100, (weekly_eggs / weekly_target) * 100) if weekly_target > 0 else 0
    
    # Prepare cards data
    cards = [
        {
            'title': 'Kuku Wote',
            'value': Chicken.objects.count(),
            'icon': 'fas fa-kiwi-bird',
            'color': 'primary'
        },
        {
            'title': 'Mayai Yote',
            'value': EggProduction.objects.aggregate(total=Sum('number_of_eggs'))['total'] or 0,
            'icon': 'fas fa-egg',
            'color': 'success'
        },
       {
    'title': 'Uatamaji Unaendelea',
    'value': Incubation.objects.filter(status='in_progress').count(),
    'icon': 'fas fa-temperature-high',
    'color': 'info'
},
     {
    'title': 'Vifaranga Wote',
    'value': Chick.objects.count(),
    'icon': 'fas fa-kiwi-bird',
    'color': 'warning'
},

        {
            'title': 'Vifo vya Kuku',
            'value': Chicken.objects.filter(is_alive=False).count(),
            'icon': 'fas fa-skull',
            'color': 'danger'
        },
        {
            'title': 'Wateja',
            'value': Customer.objects.count(),
            'icon': 'fas fa-users',
            'color': 'secondary'
        },
    ]
    
    context = {
        'cards': cards,
        'weekly_eggs': weekly_eggs,
        'weekly_target': weekly_target,
        'weekly_progress': weekly_progress,
        'recent_feedings': Feeding.objects.select_related('chicken').order_by('-feeding_time')[:5],
        'recent_health_checks': HealthStatus.objects.select_related('chicken').order_by('-checkup_date')[:5],
    }
    return render(request, 'core/home.html', context)

# Static pages
def about(request):
    return render(request, 'core/about.html')

def contact(request):
    return render(request, 'core/contact.html')

# Feeding records
def feeding(request):
    feedings = Feeding.objects.select_related('chicken').order_by('-feeding_time')
    return render(request, 'core/feeding.html', {'feedings': feedings})

# Orders view
def order(request):
    orders = Order.objects.select_related('customer', 'product').order_by('-order_date')
    products = Product.objects.all()

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.customer = request.user.customer  # Assuming logged-in user has a customer profile
            order.save()
            return redirect('order')  # redirect to same page
    else:
        form = OrderForm()

    return render(request, 'core/order.html', {
        'orders': orders,
        'products': products,
        'form': form
    })

# Health dashboard
def health_dashboard(request):
    forms = {
        'health_form': ChickenHealthStatusForm(request.POST or None),
        'disease_form': DiseaseForm(request.POST or None),
        'vaccination_form': VaccinationRecordForm(request.POST or None),
        'environment_form': ChickenEnvironmentForm(request.POST or None),
        'nutrition_form': NutritionInformationForm(request.POST or None),
        'report_form': HealthReportForm(request.POST or None),
    }

    if request.method == 'POST' and all(f.is_valid() for f in forms.values()):
        for form in forms.values():
            form.save()
        return redirect('health_dashboard')

    context = {
        **forms,
        'health_data': HealthStatus.objects.all(),
        'disease_data': Disease.objects.all(),
        'vaccination_data': VaccinationRecord.objects.all(),
        'environment_data': ChickenEnvironment.objects.all(),
        'nutrition_data': NutritionInformation.objects.all(),
        'report_data': HealthReport.objects.all(),
    }
    return render(request, 'core/health_dashboard.html', context)

# Reports with date filter
def report(request):
    from_date = request.GET.get('from_date')
    to_date = request.GET.get('to_date')
    reports = {}

    if from_date and to_date:
        from_date = timezone.datetime.strptime(from_date, '%Y-%m-%d').date()
        to_date = timezone.datetime.strptime(to_date, '%Y-%m-%d').date()

        reports = {
            'total_eggs': EggProduction.objects.filter(date_laid__range=(from_date, to_date)).aggregate(Sum('number_of_eggs'))['number_of_eggs__sum'] or 0,
            'total_chicks': Chick.objects.filter(hatch_date__range=(from_date, to_date)).aggregate(Sum('number_of_chicks'))['number_of_chicks__sum'] or 0,
            'incubations': Incubation.objects.filter(start_date__range=(from_date, to_date)).count(),
        }

    return render(request, 'core/report.html', {'reports': reports})

# Settings view
def settings(request):
    all_settings = Settings.objects.all()
    form = SettingsForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('settings')
    return render(request, 'core/settings.html', {'settings': all_settings, 'form': form})

# Calendar view
def calendar_view(request):
    # Get events from last 30 days and next 60 days
    start_date = timezone.now().date() - timedelta(days=30)
    end_date = timezone.now().date() + timedelta(days=60)
    
    events = []
    
    # Incubation events
    for incubation in Incubation.objects.filter(
        Q(start_date__range=(start_date, end_date)) | 
        Q(expected_hatch_date__range=(start_date, end_date))
    ).select_related('chicken'):
        events.append({
            'title': f"Incubation: {incubation.chicken.tag_number}",
            'start': incubation.start_date,
            'end': incubation.expected_hatch_date,
            'type': 'incubation',
            'description': f"Eggs from {incubation.chicken.tag_number} (Breed: {incubation.chicken.breed})",
            'color': '#FFD700'  # Gold color for incubation
        })
    
    # Chick hatching events
    for chick in Chick.objects.filter(hatch_date__range=(start_date, end_date)):
        events.append({
            'title': f"Hatched: {chick.number_of_chicks} chicks",
            'start': chick.hatch_date,
            'end': chick.hatch_date,
            'type': 'hatching',
            'description': f"From {chick.incubation.chicken.tag_number if chick.incubation else 'unknown'}",
            'color': '#90EE90'  # Light green for hatching
        })
    
    # Egg production events
    for egg in EggProduction.objects.filter(date_laid__range=(start_date, end_date)).select_related('chicken'):
        events.append({
            'title': f"Eggs: {egg.number_of_eggs}",
            'start': egg.date_laid,
            'end': egg.date_laid,
            'type': 'egg_production',
            'description': f"From {egg.chicken.tag_number} (Age: {egg.chicken.age} weeks)",
            'color': '#FFA07A'  # Light salmon for eggs
        })
    
    context = {
        'events': sorted(events, key=lambda x: x['start']),
        'today': timezone.now().date(),
    }
    
    return render(request, 'core/calendar.html', context)

# Chicken view
def chicken_view(request):
    chickens = Chicken.objects.all()
    return render(request, 'core/chicken.html', {'chickens': chickens})


class AddEggProductionView(CreateView):
    model = EggProduction
    fields = ['chicken', 'date_laid', 'number_of_eggs']
    template_name = 'core/add_egg_production.html'
    success_url = reverse_lazy('home')  # Rudisha kwenye homepage baada ya kuingiza rekodi
    login_url = '/login' # ukurasa wa kuingia ambao hawana ja sajiliwa kwenye accounts 
# Egg production view with email notifications
def egg_production_view(request):
    # Get search query if exists
    search_query = request.GET.get('search', '')
    
    # Get all eggs with related chicken and customer data
    eggs = EggProduction.objects.select_related('chicken__customer').order_by('-date_laid')
    
    # Apply search filter if query exists
    if search_query:
        eggs = eggs.filter(
            Q(chicken__tag_number__icontains=search_query) |
            Q(chicken__customer__name__icontains=search_query) |
            Q(date_laid__icontains=search_query)
        )
    
    # Pagination
    paginator = Paginator(eggs, 25)  # Show 25 records per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Email notifications (only for current page to avoid mass emails)
    if not search_query:  # Don't send emails when searching
        for egg in page_obj.object_list:
            try:
                if (hasattr(egg, 'chicken') and egg.chicken and 
                    hasattr(egg.chicken, 'customer') and egg.chicken.customer and
                    egg.chicken.customer.email):
                    
                    customer = egg.chicken.customer
                    message = (
                        f"Your chicken {egg.chicken.tag_number} laid {egg.number_of_eggs} "
                        f"eggs on {egg.date_laid.strftime('%B %d, %Y')}."
                    )
                    send_update_email("Egg Production Update", message, customer.email)
                    
            except Exception as e:
                logger.error(f"Error sending email for egg record {egg.id}: {e}")
                messages.error(request, f"Failed to send email notification for chicken {egg.chicken.tag_number}")
    
    context = {
        'eggs': page_obj,
        'search_query': search_query,
    }
    
    return render(request, 'core/eggproduction.html', context)
def edit_egg_production(request, pk):
    egg = get_object_or_404(EggProduction, pk=pk)
    if request.method == 'POST':
        form = EggProductionForm(request.POST, instance=egg)
        if form.is_valid():
            form.save()
            return redirect('egg_production')  # au jina halisi la view yako
    else:
        form = EggProductionForm(instance=egg)
    return render(request, 'core/edit_egg_production.html', {'form': form})
def delete_egg_production(request, pk):
    egg = get_object_or_404(EggProduction, pk=pk)
    if request.method == 'POST':
        egg.delete()
        return redirect('egg_production')  # Badilisha kama view yako ya orodha inaitwa tofauti
    return render(request, 'core/confirm_delete.html', {'object': egg})

# Incubation view
def incubation_view(request):
    incubations = Incubation.objects.all()
    return render(request, 'core/incubation.html', {'incubations': incubations})

# Chick growth view
def chick_growth_view(request):
    chicks = Chick.objects.all()
    return render(request, 'core/chick_growth.html', {'chicks': chicks})

# Customer view
def customer_view(request):
    customers = Customer.objects.all()
    return render(request, 'core/customer.html', {'customers': customers})

# Water consumption view
def water_consumption_view(request):
    water_data = WaterConsumption.objects.all()
    return render(request, 'core/water_consumption.html', {'water_data': water_data})

# Mortality view
def mortality_view(request):
    mortalities = Mortality.objects.all()
    return render(request, 'core/mortality.html', {'mortalities': mortalities})
def custom_logout(request):
    logout(request)
    return redirect('login')
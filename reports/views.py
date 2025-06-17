# reports/views.py
import json
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.db.models import Sum, Avg, Count
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta
from django.utils import timezone
from core.models import Chicken
from production.models import EggProduction, Incubation
from reports.forms import HealthReportForm
from .models import Report, CalendarEvent, HealthReport


@login_required
def report_list(request):
    reports = HealthReport.objects.all().order_by('-created_at')
    return render(request, 'reports/report_list.html', {'reports': reports})

@login_required
def add_report(request):
    if request.method == 'POST':
        form = HealthReportForm(request.POST)
        if form.is_valid():
            report = form.save(commit=False)
            report.created_by = request.user
            report.save()
            return redirect('reports:report_list')
    else:
        form = HealthReportForm()
    return render(request, 'reports/report_form.html', {'form': form})

def view_report(request, pk):
    report = get_object_or_404(HealthReport, pk=pk)
    return render(request, 'reports/view_report.html', {'report': report})

def edit_report(request, pk):
    report = get_object_or_404(HealthReport, pk=pk)
    if request.method == 'POST':
        form = HealthReportForm(request.POST, instance=report)
        if form.is_valid():
            form.save()
            return redirect('core:view_report', pk=report.pk)
    else:
        form = HealthReportForm(instance=report)
    return render(request, 'reports/report_form.html', {'form': form})

def delete_report(request, pk):
    report = get_object_or_404(HealthReport, pk=pk)
    if request.method == 'POST':
        report.delete()
        return redirect('core:report_list')
    return render(request, 'reports/report_confirm_delete.html', {'report': report})


@login_required
def production_report(request):
    # Default to last 30 days
    end_date = timezone.now().date()
    start_date = end_date - timedelta(days=30)
    
    # Get filter parameters from request
    if request.GET.get('start_date'):
        start_date = datetime.strptime(request.GET['start_date'], '%Y-%m-%d').date()
    if request.GET.get('end_date'):
        end_date = datetime.strptime(request.GET['end_date'], '%Y-%m-%d').date()
    
    # Aggregate data
    eggs_data = EggProduction.objects.filter(
        date_laid__range=(start_date, end_date)
    ).values('date_laid__month', 'date_laid__year').annotate(
        total_eggs=Sum('number_of_eggs'),
        avg_weight=Avg('weight')
    ).order_by('date_laid__year', 'date_laid__month')
    
    # Quality distribution
    quality_data = EggProduction.objects.filter(
        date_laid__range=(start_date, end_date)
    ).values('quality').annotate(
        count=Count('id')
    ).order_by('-count')
    
    context = {
        'eggs_data': list(eggs_data),
        'quality_data': list(quality_data),
        'start_date': start_date.strftime('%Y-%m-%d'),
        'end_date': end_date.strftime('%Y-%m-%d'),
        'time_range': f"{start_date.strftime('%b %d, %Y')} - {end_date.strftime('%b %d, %Y')}"
    }
    
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse(context)
    
    return render(request, 'reports/production.html', context)

@login_required
def financial_report(request):
    end_date = timezone.now().date()
    start_date = end_date - timedelta(days=365)
    
    context = {
        'start_date': start_date.strftime('%Y-%m-%d'),
        'end_date': end_date.strftime('%Y-%m-%d')
    }
    
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse(context)
    
    return render(request, 'reports/financial.html', context)

@login_required
def health_report(request):
    end_date = timezone.now().date()
    start_date = end_date - timedelta(days=90)
    
    reports = HealthReport.objects.filter(
        created_at__date__range=(start_date, end_date)
    ).order_by('-created_at')
    
    context = {
        'reports': reports,
        'start_date': start_date.strftime('%Y-%m-%d'),
        'end_date': end_date.strftime('%Y-%m-%d')
    }
    
    return render(request, 'reports/health.html', context)

@login_required
def calendar_events(request):
    start = request.GET.get('start')
    end = request.GET.get('end')
    
    events = CalendarEvent.objects.filter(
        start_date__gte=start,
        end_date__lte=end
    ).values(
        'id', 'title', 'start_date', 'end_date', 'all_day',
        'event_type', 'category', 'is_completed'
    )
    
    return JsonResponse(list(events), safe=False)
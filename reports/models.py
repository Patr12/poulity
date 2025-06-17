import json
from django.db import models, transaction
from django.contrib.auth.models import User
# Create your models here.
from django.utils import timezone
from django.forms import ValidationError
from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Sum, Count
from datetime import datetime, timedelta
from core.models import EVENT_TYPES, Chicken, Order
from production.models import EggProduction


class CalendarEvent(models.Model):
    EVENT_CATEGORIES = [
        ('production', 'Production'),
        ('health', 'Health'),
        ('financial', 'Financial'),
        ('maintenance', 'Maintenance'),
        ('other', 'Other')
    ]
    
    title = models.CharField(max_length=200)
    event_type = models.CharField(max_length=20, choices=EVENT_TYPES)
    category = models.CharField(max_length=20, choices=EVENT_CATEGORIES, default='production')
    start_date = models.DateTimeField()
    end_date = models.DateTimeField(null=True, blank=True)
    all_day = models.BooleanField(default=False)
    description = models.TextField(blank=True)
    location = models.CharField(max_length=200, blank=True)
    related_chicken = models.ForeignKey(Chicken, on_delete=models.SET_NULL, null=True, blank=True)
    related_order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_completed = models.BooleanField(default=False)
    priority = models.PositiveSmallIntegerField(default=2, choices=[
        (1, 'High'),
        (2, 'Medium'),
        (3, 'Low')
    ])
    
    class Meta:
        ordering = ['start_date']
    
    def __str__(self):
        return f"{self.title} ({self.get_event_type_display()})"
    
    @property
    def duration(self):
        if not self.end_date:
            return None
        return self.end_date - self.start_date
    
    def clean(self):
        if self.end_date and self.end_date < self.start_date:
            raise ValidationError("End date cannot be before start date")
    
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

class Report(models.Model):
    REPORT_TYPES = [
        ('production', 'Egg Production'),
        ('health', 'Health Status'),
        ('financial', 'Financial'),
        ('inventory', 'Inventory'),
        ('custom', 'Custom')
    ]
    
    FREQUENCY_CHOICES = [
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('quarterly', 'Quarterly'),
        ('yearly', 'Yearly'),
        ('adhoc', 'Ad Hoc')
    ]
    
    title = models.CharField(max_length=200)
    report_type = models.CharField(max_length=20, choices=REPORT_TYPES)
    frequency = models.CharField(max_length=20, choices=FREQUENCY_CHOICES, default='weekly')
    content = models.TextField(blank=True)
    parameters = models.JSONField(default=dict, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_generated = models.DateTimeField(null=True, blank=True)
    is_automated = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} ({self.get_report_type_display()})"
    
    def generate_report(self, start_date=None, end_date=None):
        """Generate report content based on type"""
        report_data = {}
        
        if self.report_type == 'production':
            qs = EggProduction.objects.all()
            if start_date:
                qs = qs.filter(date_laid__gte=start_date)
            if end_date:
                qs = qs.filter(date_laid__lte=end_date)
                
            report_data = {
                'total_eggs': qs.aggregate(total=Sum('number_of_eggs'))['total'] or 0,
                'average_per_chicken': qs.values('chicken').annotate(
                    total=Sum('number_of_eggs')
                ).aggregate(avg=Avg('total'))['avg'] or 0,
                'by_quality': qs.values('quality').annotate(
                    total=Sum('number_of_eggs')
                ).order_by('-total')
            }
        
        elif self.report_type == 'health':
            # Similar logic for health reports
            pass
        
        self.content = json.dumps(report_data, indent=2)
        self.last_generated = timezone.now()
        self.save()
        return report_data
            
def production_report(request):
    # Last 12 months data
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=365)
    
    eggs_data = EggProduction.objects.filter(
        date_laid__range=(start_date, end_date)
    ).values('date_laid__month').annotate(
        total_eggs=Sum('number_of_eggs'),
        damaged_eggs=Sum('damaged_eggs')
    ).order_by('date_laid__month')
    
    context = {
        'eggs_data': list(eggs_data),
        'start_date': start_date,
        'end_date': end_date,
    }
    
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse(context)
    
    return render(request, 'reports/production.html', context)

def financial_report(request):
    # Last 12 months data
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=365)
    
    income_data = Income.objects.filter(
        date__range=(start_date, end_date)
    ).values('date__month').annotate(
        total=Sum('amount')
    ).order_by('date__month')
    
    expense_data = Expense.objects.filter(
        date__range=(start_date, end_date)
    ).values('date__month').annotate(
        total=Sum('amount')
    ).order_by('date__month')
    
    context = {
        'income_data': list(income_data),
        'expense_data': list(expense_data),
        'start_date': start_date,
        'end_date': end_date,
    }
    
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse(context)
    
    return render(request, 'reports/financial.html', context)
# ==== Ripoti ya Afya ====
class HealthReport(models.Model):
    health_checkup = models.TextField(verbose_name="Uchunguzi wa Afya")
    vet_report = models.TextField(verbose_name="Ripoti ya Daktari wa Wanyama")
    resolved = models.BooleanField(default=False, verbose_name="Imekamilika")
    created_at = models.DateTimeField(default=timezone.now, verbose_name="Tarehe ya Kuundwa")
    
    class Meta:
        db_table = 'core_healthreport'  # Explicit table name
        verbose_name = "Ripoti ya Afya"
        verbose_name_plural = "Ripoti za Afya"
        ordering = ['-created_at']

    def __str__(self):
        return f"Ripoti ya Afya ya {self.created_at.strftime('%Y-%m-%d')}"
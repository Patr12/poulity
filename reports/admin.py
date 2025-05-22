from django.contrib import admin
from .models import CalendarEvent, Report, HealthReport


@admin.register(CalendarEvent)
class CalendarEventAdmin(admin.ModelAdmin):
    list_display = ('title', 'event_type', 'category', 'start_date', 'end_date', 'is_completed', 'priority')
    list_filter = ('event_type', 'category', 'is_completed', 'priority')
    search_fields = ('title', 'description', 'location')
    date_hierarchy = 'start_date'
    ordering = ('-start_date',)


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('title', 'report_type', 'frequency', 'created_by', 'created_at', 'last_generated', 'is_automated')
    list_filter = ('report_type', 'frequency', 'is_automated')
    search_fields = ('title', 'content')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)


@admin.register(HealthReport)
class HealthReportAdmin(admin.ModelAdmin):
    list_display = ('health_checkup', 'vet_report', 'created_at')
    search_fields = ('health_checkup', 'vet_report')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)


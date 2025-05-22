# your_app/admin.py
from django.contrib import admin
from .models import Breed, Chicken, Order, Report, Feeding, Settings

@admin.register(Breed)
class BreedAdmin(admin.ModelAdmin):
    list_display = ('name', 'egg_production_rate', 'maturity_age')
    search_fields = ('name',)

@admin.register(Chicken)
class ChickenAdmin(admin.ModelAdmin):
    list_display = ('tag_number', 'breed', 'owner', 'customer', 'gender', 'is_alive', 'age', 'last_health_check')
    list_filter = ('breed', 'gender', 'is_alive')
    search_fields = ('tag_number', 'owner__name', 'customer__name')
    readonly_fields = ('age', 'total_eggs_produced')
    fieldsets = (
        (None, {
            'fields': ('tag_number', 'breed', 'owner', 'customer', 'gender', 'date_acquired', 'date_of_birth', 'parent', 'is_alive', 'last_health_check', 'notes')
        }),
        ('Statistics', {
            'fields': ('age', 'total_eggs_produced'),
        }),
    )

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('product', 'quantity', 'customer', 'order_date')
    list_filter = ('order_date',)
    search_fields = ('product', 'customer__name')

@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')
    search_fields = ('title',)
    list_filter = ('created_at',)

@admin.register(Feeding)
class FeedingAdmin(admin.ModelAdmin):
    list_display = ('chicken', 'feed_type', 'quantity', 'feeding_time')
    search_fields = ('chicken__tag_number', 'feed_type')
    list_filter = ('feeding_time',)

@admin.register(Settings)
class SettingsAdmin(admin.ModelAdmin):
    list_display = ('key', 'value')
    search_fields = ('key',)

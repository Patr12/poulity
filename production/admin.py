from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import EggProduction, Incubation, Product

@admin.register(EggProduction)
class EggProductionAdmin(admin.ModelAdmin):
    list_display = ('chicken', 'date_laid', 'number_of_eggs', 'quality', 'collected_by')
    list_filter = ('quality', 'date_laid')
    search_fields = ('chicken__tag_number', 'collected_by__username')
    autocomplete_fields = ['chicken', 'collected_by']
    date_hierarchy = 'date_laid'

@admin.register(Incubation)
class IncubationAdmin(admin.ModelAdmin):
    list_display = ('id', 'chicken', 'start_date', 'expected_hatch_date', 'status', 'is_hatched')
    list_filter = ('status', 'start_date')
    search_fields = ('chicken__tag_number',)
    autocomplete_fields = ['chicken', 'eggs']
    date_hierarchy = 'start_date'

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category')
    list_filter = ('category',)
    search_fields = ('name',)

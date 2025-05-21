from django.contrib import admin
from django.contrib import admin
from .models import Chicken, EggProduction, Incubation, Chick, Customer, Mortality, Order, Calendar

@admin.register(Chicken)
class ChickenAdmin(admin.ModelAdmin):
    list_display = ('tag_number', 'breed', 'date_acquired')
    search_fields = ('tag_number', 'breed')
    list_filter = ('breed', 'date_acquired')

@admin.register(EggProduction)
class EggProductionAdmin(admin.ModelAdmin):
    list_display = ('chicken', 'date_laid', 'number_of_eggs')
    search_fields = ('chicken__tag_number',)
    list_filter = ('date_laid',)

@admin.register(Incubation)
class IncubationAdmin(admin.ModelAdmin):
    list_display = ('chicken', 'start_date', 'expected_hatch_date', 'is_hatched')
    search_fields = ('chicken__tag_number',)
    list_filter = ('is_hatched', 'start_date')

@admin.register(Chick)
class ChickAdmin(admin.ModelAdmin):
    list_display = ('incubation', 'number_of_chicks', 'hatch_date')
    list_filter = ('hatch_date',)

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone')
    search_fields = ('name', 'email', 'phone')

admin.site.register(Mortality),   
admin.site.register(Calendar),
admin.site.register(Order), 

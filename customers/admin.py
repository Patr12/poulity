from django.contrib import admin
from django.contrib import admin
from .models import Customer

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'customer_type', 'registration_date')
    search_fields = ('name', 'email', 'phone')
    list_filter = ('customer_type', 'registration_date')

from django.contrib import admin
from .models import Designation, Staff, Salary

@admin.register(Designation)
class DesignationAdmin(admin.ModelAdmin):
    list_display = ('title', 'department', 'base_salary')
    search_fields = ('title', 'department')
    list_filter = ('department',)

@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ('user_full_name', 'designation', 'hire_date', 'phone', 'emergency_contact')
    search_fields = ('user__first_name', 'user__last_name', 'phone')
    list_filter = ('designation', 'hire_date')

    def user_full_name(self, obj):
        return obj.user.get_full_name()
    user_full_name.short_description = 'Full Name'

@admin.register(Salary)
class SalaryAdmin(admin.ModelAdmin):
    list_display = ('staff', 'month', 'basic_salary', 'bonus', 'deductions', 'net_salary', 'payment_date')
    search_fields = ('staff__user__first_name', 'staff__user__last_name')
    list_filter = ('month', 'payment_date')

    def net_salary(self, obj):
        return obj.net_salary
    net_salary.short_description = 'Net Salary'

from django.contrib import admin
from .models import Order, OrderItem, Payment


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('subtotal',)
    fields = ('product', 'quantity', 'unit_price', 'subtotal')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'customer', 'status', 'payment_method', 'payment_status', 'order_date', 'total_amount')
    list_filter = ('status', 'payment_method', 'payment_status', 'order_date')
    search_fields = ('order_number', 'customer__name')
    inlines = [OrderItemInline]
    readonly_fields = ('order_date', 'total_amount')


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('order', 'amount', 'receipt_number', 'payment_method', 'payment_date', 'confirmed_by')
    list_filter = ('payment_method', 'payment_date')
    search_fields = ('order__order_number', 'receipt_number')

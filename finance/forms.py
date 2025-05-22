from django import forms
from django.forms import inlineformset_factory
from .models import Order, OrderItem, Payment

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['customer', 'order_number', 'status', 'payment_method', 'delivery_address', 'notes']

OrderItemFormSet = inlineformset_factory(
    Order, OrderItem,
    fields=['product', 'quantity', 'unit_price'],
    extra=1,
    can_delete=True
)

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['amount', 'receipt_number']

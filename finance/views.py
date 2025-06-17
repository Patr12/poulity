from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Order, OrderItem, Payment
from .forms import OrderForm, OrderItemFormSet, PaymentForm

@login_required
def order_list(request):
    orders = Order.objects.select_related('customer').all()
    return render(request, 'orders/order_list.html', {'orders': orders})

@login_required
def order_detail(request, pk):
    order = get_object_or_404(Order, pk=pk)
    return render(request, 'orders/order_detail.html', {'order': order})

@login_required
def create_order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        formset = OrderItemFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            order = form.save()
            formset.instance = order
            formset.save()
            return redirect('order_list')
    else:
        form = OrderForm()
        formset = OrderItemFormSet()
    return render(request, 'orders/create_order.html', {'form': form, 'formset': formset})

@login_required
def make_payment(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            order.process_payment(
                amount=form.cleaned_data['amount'],
                receipt_number=form.cleaned_data['receipt_number']
            )
            return redirect('order_detail', pk=order.id)
    else:
        form = PaymentForm()
    return render(request, 'orders/make_payment.html', {'form': form, 'order': order})

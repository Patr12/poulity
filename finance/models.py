
from django.db import models, transaction
from django.forms import ValidationError
from django.contrib.auth.models import User



# Create your models here.

class Order(models.Model):
    ORDER_STATUS = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled')
    ]
    
    PAYMENT_METHODS = [
        ('cash', 'Cash'),
        ('mpesa', 'M-Pesa'),
        ('credit', 'Credit'),
        ('bank', 'Bank Transfer'),
        ('other', 'Other')
    ]
    
    customer = models.ForeignKey('customers.Customer', on_delete=models.PROTECT,         related_name='finance_orders'  # Unique related_name
    )
    order_number = models.CharField(max_length=20, unique=True)
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=ORDER_STATUS, default='pending')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS)
    payment_status = models.BooleanField(default=False)
    delivery_address = models.TextField()
    notes = models.TextField(blank=True)
    
    class Meta:
        ordering = ['-order_date']
    
    def __str__(self):
        return f"Order #{self.order_number} - {self.customer.name}"
    
    @property
    def total_amount(self):
        return sum(item.subtotal for item in self.items.all())
    
    @transaction.atomic
    def process_payment(self, amount, receipt_number):
        if self.payment_status:
            raise ValidationError("Payment already processed")
        
        Payment.objects.create(
            order=self,
            amount=amount,
            receipt_number=receipt_number,
            payment_method=self.payment_method
        )
        
        self.payment_status = True
        if self.status == 'pending':
            self.status = 'processing'
        self.save()

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    
    class Meta:
        verbose_name = 'Order Item'
        verbose_name_plural = 'Order Items'
    
    def __str__(self):
        return f"{self.quantity} x {self.product} for order #{self.order.order_number}"
    
    @property
    def subtotal(self):
        return self.quantity * self.unit_price

class Payment(models.Model):
    order = models.ForeignKey(Order, on_delete=models.PROTECT, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    receipt_number = models.CharField(max_length=50)
    payment_method = models.CharField(max_length=20, choices=Order.PAYMENT_METHODS)
    payment_date = models.DateTimeField(auto_now_add=True)
    confirmed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    
    class Meta:
        ordering = ['-payment_date']
    
    def __str__(self):
        return f"Payment of {self.amount} for order #{self.order.order_number}"

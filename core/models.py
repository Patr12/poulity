from django.db import models, transaction
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from datetime import date
from health.models import Mortality
from production.models import EggProduction, Product


class Breed(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    egg_production_rate = models.CharField(max_length=50)
    maturity_age = models.PositiveIntegerField(help_text="In weeks")
    
    def __str__(self):
        return self.name

# ==== Kuku ====
class Chicken(models.Model):
    GENDER_CHOICES = [('M', 'Male'), ('F', 'Female'), ('U', 'Unknown')]
    owner = models.ForeignKey('customers.Customer', on_delete=models.CASCADE, related_name='chickens', blank=True, null=True)    
    customer = models.ForeignKey('customers.Customer', on_delete=models.CASCADE, null=True, blank=True)
    tag_number = models.CharField(max_length=20, unique=True)
    breed = models.ForeignKey(Breed, on_delete=models.PROTECT)
    date_acquired = models.DateField()
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='U')
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
    is_alive = models.BooleanField(default=True)
    last_health_check = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True)
    
    class Meta:
        ordering = ['tag_number']
        verbose_name_plural = 'Chickens'
    
    def __str__(self):
        status = "Alive" if self.is_alive else "Deceased"
        return f"{self.tag_number} - {self.breed.name} ({status})"
    
    @property
    def age(self):
        """Calculate age in weeks"""
        reference_date = self.date_of_birth or self.date_acquired
        if reference_date is None:
         return None  # Or return 0 or "Unknown"
        delta = date.today() - reference_date
        return delta.days // 7
    
    @property
    def total_eggs_produced(self):
        return self.egg_productions.aggregate(total=Sum('number_of_eggs'))['total'] or 0
    
    def mark_as_deceased(self, reason, date=None):
        with transaction.atomic():
            self.is_alive = False
            self.save()
            Mortality.objects.create(
                chicken=self,
                reason=reason,
                count=1,
                date=date or date.today()
            )



# ==== Oda ====
class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]

    customer = models.ForeignKey('customers.Customer', on_delete=models.CASCADE, related_name='orders')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
# Or replace with ForeignKey to Product model
    quantity = models.PositiveIntegerField()
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"Order: {self.product} x {self.quantity} by {self.customer.name} ({self.status})"

    class Meta:
        ordering = ['-order_date']

# ==== Ripoti ====
class Report(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


# ==== Ulishaji ====
class Feeding(models.Model):
    chicken = models.ForeignKey(Chicken, on_delete=models.CASCADE, related_name='feedings')
    feed_type = models.CharField(max_length=100)
    quantity = models.FloatField(help_text="Kiasi cha chakula (kg/l)")
    feeding_time = models.DateTimeField()

    def __str__(self):
        return f"{self.chicken.tag_number} fed {self.feed_type} at {self.feeding_time}"





# ==== Mipangilio ya Mfumo ====
class Settings(models.Model):
    key = models.CharField(max_length=100, unique=True)
    value = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.key}: {self.value}"

# ==== Kalenda za Matukio ====
EVENT_TYPES = [
    ('laying', 'Kuku Kutaga'),
    ('brooding', 'Kuatamia'),
    ('hatching', 'Kutotoresha'),
    ('vaccination', 'Chanjo'),
    ('order', 'Oda ya Mteja'),
]



# ==== Helper for ACID Compliance ====
# Example transactional save
@transaction.atomic
def register_egg_production(chicken, date, number):
    if number < 1:
        raise ValidationError("Idadi ya mayai lazima iwe zaidi ya sifuri.")
    return EggProduction.objects.create(chicken=chicken, date_laid=date, number_of_eggs=number)

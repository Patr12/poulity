from datetime import date
from django.db import models

# Create your models here.
# production/models.py
from django.db import models, transaction
from django.contrib.auth.models import User



class Flock(models.Model):
    farm = models.ForeignKey('customers.Customer', on_delete=models.CASCADE)
    breed = models.ForeignKey('core.Breed', on_delete=models.SET_NULL, null=True)
    batch_number = models.CharField(max_length=50)
    arrival_date = models.DateField()
    quantity = models.PositiveIntegerField()
    current_stock = models.PositiveIntegerField()
    notes = models.TextField(blank=True)
    
    def __str__(self):
        return f"Batch {self.batch_number} ({self.breed})"


class Chick(models.Model):
    chicken = models.ForeignKey(
        'core.Chicken',
        on_delete=models.CASCADE,
        related_name='inventory_chicks'
    )
    hatch_date = models.DateField()
    source_incubation = models.ForeignKey(
        'production.Incubation',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    number_of_chicks = models.PositiveIntegerField(default=0)

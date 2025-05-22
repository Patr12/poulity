from datetime import date
from django.db import models, transaction
from django.contrib.auth.models import User
from django.forms import ValidationError
from inventory.models import Chick


class EggProduction(models.Model):
    EGG_QUALITY_CHOICES = [
        ('grade_a', 'Grade A'),
        ('grade_b', 'Grade B'),
        ('grade_c', 'Grade C'),
        ('cracked', 'Cracked'),
        ('dirty', 'Dirty')
    ]
    
    chicken = models.ForeignKey('core.Chicken', on_delete=models.CASCADE, related_name='production_eggs')
    date_laid = models.DateField()
    number_of_eggs = models.PositiveIntegerField(default=1)
    quality = models.CharField(max_length=20, choices=EGG_QUALITY_CHOICES, default='grade_a')
    weight = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, help_text="Average weight per egg in grams")
    collected_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    notes = models.TextField(blank=True)
    
    class Meta:
        ordering = ['-date_laid']
        unique_together = ['chicken', 'date_laid']
        verbose_name_plural = 'Egg Productions'
    
    def __str__(self):
        return f"{self.chicken.tag_number} - {self.number_of_eggs} eggs on {self.date_laid}"
    
    def clean(self):
        if self.date_laid > date.today():
            raise ValidationError("Date laid cannot be in the future")
        if not self.chicken.is_alive:
            raise ValidationError("Cannot record eggs for deceased chicken")
    
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
    
class Incubation(models.Model):
    INCUBATION_STATUS = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('successful', 'Successful'),
        ('failed', 'Failed'),
        ('cancelled', 'Cancelled')
    ]
    
    chicken = models.ForeignKey('core.Chicken', on_delete=models.CASCADE, related_name='incubations')
    eggs = models.ManyToManyField(EggProduction, related_name='incubations')
    start_date = models.DateField()
    expected_hatch_date = models.DateField()
    actual_hatch_date = models.DateField(null=True, blank=True)
    temperature = models.DecimalField(max_digits=5, decimal_places=2, help_text="In Celsius")
    humidity = models.DecimalField(max_digits=5, decimal_places=2, help_text="Percentage")
    status = models.CharField(max_length=20, choices=INCUBATION_STATUS, default='pending')
    notes = models.TextField(blank=True)
    is_hatched = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-start_date']
        verbose_name_plural = 'Incubations'
    
    def __str__(self):
        return f"Incubation #{self.id} - {self.chicken.tag_number}"
    
    @property
    def duration(self):
        """Return incubation duration in days"""
        end_date = self.actual_hatch_date or self.expected_hatch_date
        return (end_date - self.start_date).days
    
    @transaction.atomic
    def mark_as_hatched(self, hatch_date, number_of_chicks):
        self.actual_hatch_date = hatch_date
        self.status = 'successful'
        self.is_hatched = True  # Set this flag
        self.save()
        
        Chick.objects.create(
            incubation=self,
            number_of_chicks=number_of_chicks,
            hatch_date=hatch_date
        )
        
        # Update egg status if needed
        self.eggs.update(incubated=True)  

    def is_hatched(self):
        return self.hatch_date is not None     

# models.py
class Product(models.Model):
    CATEGORY_CHOICES = [
        ('kuku', 'Kuku'),
        ('mayai', 'Mayai'),
        ('incubation', 'Incubation'),
    ]
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)

    def __str__(self):
        return f"{self.name} ({self.get_category_display()})"



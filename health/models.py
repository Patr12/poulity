from django.db import models
# Create your models here.# health/models.py
from django.db import models, transaction
from django.contrib.auth.models import User

class Disease(models.Model):
    SEVERITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical')
    ]
    
    name = models.CharField(max_length=100, unique=True)
    scientific_name = models.CharField(max_length=100, blank=True)
    description = models.TextField()
    symptoms = models.TextField()
    treatment = models.TextField()
    prevention = models.TextField()
    severity = models.CharField(max_length=20, choices=SEVERITY_CHOICES)
    zoonotic = models.BooleanField(default=False, help_text="Can be transmitted to humans")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name} ({self.get_severity_display()})"

class Vaccination(models.Model):
    name = models.CharField(max_length=100)
    disease = models.ForeignKey(Disease, on_delete=models.CASCADE, related_name='vaccines')
    dosage = models.CharField(max_length=100)
    frequency = models.CharField(max_length=100, help_text="How often it should be administered")
    duration = models.CharField(max_length=100, help_text="How long it provides protection")
    notes = models.TextField(blank=True)
    
    class Meta:
        ordering = ['name']
        unique_together = ['name', 'disease']
    
    def __str__(self):
        return f"{self.name} for {self.disease.name}"

class VaccinationRecord(models.Model):
    chicken = models.ForeignKey('core.Chicken', on_delete=models.CASCADE, related_name='vaccinations')
    vaccine = models.ForeignKey(Vaccination, on_delete=models.PROTECT)
    date_administered = models.DateField()
    next_due_date = models.DateField()
    administered_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    batch_number = models.CharField(max_length=50, blank=True)
    notes = models.TextField(blank=True)
    
    class Meta:
        ordering = ['-date_administered']
    
    def __str__(self):
        return f"{self.vaccine.name} for {self.chicken.tag_number} on {self.date_administered}"
    

# ==== Vifo vya Kuku ====
class Mortality(models.Model):
    chicken = models.ForeignKey(
        'core.Chicken',
        on_delete=models.CASCADE,
        related_name='health_mortalities'  # Unique related_name
    )
    date = models.DateField()
    reason = models.TextField()
    
    def __str__(self):
        return f"Mortality of {self.chicken.tag_number}"
# ==== Matumizi ya Maji ====
class WaterConsumption(models.Model):
    chicken = models.ForeignKey('core.Chicken', on_delete=models.CASCADE, related_name='water_usages')
    liters = models.FloatField()
    date = models.DateField()

    def __str__(self):
        return f"{self.chicken.tag_number} used {self.liters} L on {self.date}"

# ==== Afya ya Kuku ====
class HealthStatus(models.Model):
    HEALTH_CHOICES = [('Healthy', 'Healthy'), ('Sick', 'Sick'), ('Dead', 'Dead')]
    chicken = models.ForeignKey('core.Chicken', on_delete=models.CASCADE, related_name='health_checks')
    status = models.CharField(max_length=200, choices=HEALTH_CHOICES)
    count = models.PositiveIntegerField(null=True, blank=True)
    checkup_date = models.DateField()

    def __str__(self):
        return f"{self.chicken.tag_number} status: {self.status} on {self.checkup_date}"


# ==== Mazingira ya Kuku ====
class ChickenEnvironment(models.Model):
    temperature = models.CharField(max_length=20)
    humidity = models.CharField(max_length=20)
    cleanliness = models.CharField(max_length=20)
    stocking_density = models.CharField(max_length=50)
    recorded_at = models.DateTimeField(auto_now_add=True)

# ==== Lishe ====
class NutritionInformation(models.Model):
    feed_type = models.CharField(max_length=100)
    feeding_schedule = models.CharField(max_length=100)
    food_consumption_kg = models.FloatField()
    water_consumption_ml = models.FloatField()
    recorded_at = models.DateTimeField(auto_now_add=True)
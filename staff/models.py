from django.db import models

# Create your models here.
# staff/models.py
from django.db import models
from django.contrib.auth.models import User

class Designation(models.Model):
    title = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    description = models.TextField()
    base_salary = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return self.title

class Staff(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    designation = models.ForeignKey(Designation, on_delete=models.SET_NULL, null=True)
    hire_date = models.DateField()
    phone = models.CharField(max_length=20)
    address = models.TextField()
    emergency_contact = models.CharField(max_length=100)
    
    def __str__(self):
        return f"{self.user.get_full_name()} ({self.designation})"

class Salary(models.Model):
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    month = models.DateField()
    basic_salary = models.DecimalField(max_digits=10, decimal_places=2)
    bonus = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    deductions = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    payment_date = models.DateField()
    notes = models.TextField(blank=True)
    
    @property
    def net_salary(self):
        return self.basic_salary + self.bonus - self.deductions
    
    def __str__(self):
        return f"Salary for {self.staff} - {self.month.strftime('%B %Y')}"
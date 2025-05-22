from django.db import models
from django.db import models, transaction
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

# Create your models here.
class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='customer_profile', null=True, blank=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, validators=[RegexValidator(r'^\+?1?\d{9,15}$')])
    address = models.TextField(blank=True)
    registration_date = models.DateField(auto_now_add=True)
    customer_type = models.CharField(max_length=20, choices=[
        ('individual', 'Individual'),
        ('business', 'Business'),
        ('farmer', 'Farmer')
    ], default='individual')
    
    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Customers'
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.user and self.email:
            # Auto-create user if email provided but no user linked
            username = self.email.split('@')[0]
            self.user, created = User.objects.get_or_create(
                email=self.email,
                defaults={'username': username}
            )
        super().save(*args, **kwargs)
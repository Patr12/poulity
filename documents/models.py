from datetime import date
import os
from django.db import models, transaction
from django.contrib.auth.models import User

# Create your models here.
# documents/models.py
from django.db import models
class DocumentCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = 'Document Categories'
        ordering = ['name']
    
    def __str__(self):
        return self.name

class FarmDocument(models.Model):
    DOCUMENT_TYPES = [
        ('contract', 'Contract'),
        ('certificate', 'Certificate'),
        ('report', 'Report'),
        ('manual', 'Manual'),
        ('other', 'Other')
    ]
    
    title = models.CharField(max_length=200)
    document_type = models.CharField(max_length=20, choices=DOCUMENT_TYPES)
    category = models.ForeignKey(DocumentCategory, on_delete=models.SET_NULL, null=True, blank=True)
    file = models.FileField(upload_to='documents/%Y/%m/%d/')
    description = models.TextField(blank=True)
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    upload_date = models.DateTimeField(auto_now_add=True)
    expiry_date = models.DateField(null=True, blank=True)
    is_confidential = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-upload_date']
    
    def __str__(self):
        return self.title
    
    @property
    def file_extension(self):
        return os.path.splitext(self.file.name)[1].lower()
    
    @property
    def is_expired(self):
        return self.expiry_date and self.expiry_date < date.today()
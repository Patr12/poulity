from django import forms
from .models import FarmDocument


class FarmDocumentForm(forms.ModelForm):
    class Meta:
        model = FarmDocument
        fields = [
            'title', 'document_type', 'category',
            'file', 'description', 'expiry_date', 'is_confidential'
        ]

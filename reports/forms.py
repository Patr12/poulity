from django import forms
from .models import HealthReport

class HealthReportForm(forms.ModelForm):
    class Meta:
        model = HealthReport
        fields = ['health_checkup', 'vet_report', 'resolved']
        widgets = {
            'health_checkup': forms.Textarea(attrs={'rows': 4}),
            'vet_report': forms.Textarea(attrs={'rows': 4}),
        }
        labels = {
            'health_checkup': 'Uchunguzi wa Afya',
            'vet_report': 'Ripoti ya Daktari',
            'resolved': 'Imekamilika',
        }
from django import forms
from health.models import ChickenEnvironment, Disease, HealthStatus, NutritionInformation, VaccinationRecord
from reports.models import CalendarEvent, HealthReport
from .models import Settings
from .models import EggProduction

class EggProductionForm(forms.ModelForm):
    class Meta:
        model = EggProduction
        fields = ['chicken', 'date_laid', 'number_of_eggs']  # ongeza fields zako halisi


class ChickenHealthStatusForm(forms.ModelForm):
    class Meta:
        model = HealthStatus
        fields = ['status', 'count']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-control'}),
            'count': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class DiseaseForm(forms.ModelForm):
    class Meta:
        model = Disease
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }

class VaccinationRecordForm(forms.ModelForm):
    class Meta:
        model = VaccinationRecord
        fields = ['vaccine', 'date_administered', 'next_due_date', 'administered_by', 'batch_number', 'notes']
        widgets = {
            'vaccine': forms.Select(attrs={'class': 'form-control'}),
            'date_administered': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'next_due_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'administered_by': forms.Select(attrs={'class': 'form-control'}),
            'batch_number': forms.TextInput(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }


class ChickenEnvironmentForm(forms.ModelForm):
    class Meta:
        model = ChickenEnvironment
        fields = ['temperature', 'humidity', 'cleanliness', 'stocking_density']
        widgets = {
            'temperature': forms.TextInput(attrs={'class': 'form-control'}),
            'humidity': forms.TextInput(attrs={'class': 'form-control'}),
            'cleanliness': forms.TextInput(attrs={'class': 'form-control'}),
            'stocking_density': forms.TextInput(attrs={'class': 'form-control'}),
        }

class NutritionInformationForm(forms.ModelForm):
    class Meta:
        model = NutritionInformation
        fields = ['feed_type', 'feeding_schedule', 'food_consumption_kg', 'water_consumption_ml']
        widgets = {
            'feed_type': forms.TextInput(attrs={'class': 'form-control'}),
            'feeding_schedule': forms.TextInput(attrs={'class': 'form-control'}),
            'food_consumption_kg': forms.NumberInput(attrs={'class': 'form-control'}),
            'water_consumption_ml': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class HealthReportForm(forms.ModelForm):
    class Meta:
        model = HealthReport
        fields = ['health_checkup', 'vet_report']
        widgets = {
            'health_checkup': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'vet_report': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }


class SettingsForm(forms.ModelForm):
    class Meta:
        model = Settings
        fields = ['key', 'value']


# callenda
class CalendarEventForm(forms.ModelForm):
    class Meta:
        model = CalendarEvent
        fields = ['title', 'event_type', 'category', 'start_date', 'end_date', 'description']
        widgets = {
            'start_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'description': forms.Textarea(attrs={'rows': 3}),
        }
   
        

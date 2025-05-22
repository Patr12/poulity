from django import forms
from .models import *

class DiseaseForm(forms.ModelForm):
    class Meta:
        model = Disease
        fields = '__all__'

class VaccinationForm(forms.ModelForm):
    class Meta:
        model = Vaccination
        fields = '__all__'

class VaccinationRecordForm(forms.ModelForm):
    class Meta:
        model = VaccinationRecord
        fields = '__all__'

class MortalityForm(forms.ModelForm):
    class Meta:
        model = Mortality
        fields = '__all__'

class WaterConsumptionForm(forms.ModelForm):
    class Meta:
        model = WaterConsumption
        fields = '__all__'

class HealthStatusForm(forms.ModelForm):
    class Meta:
        model = HealthStatus
        fields = '__all__'

class ChickenEnvironmentForm(forms.ModelForm):
    class Meta:
        model = ChickenEnvironment
        fields = '__all__'

class NutritionInformationForm(forms.ModelForm):
    class Meta:
        model = NutritionInformation
        fields = '__all__'

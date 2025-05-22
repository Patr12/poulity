# forms.py
from django import forms
from core.models import Order
from .models import EggProduction, Incubation, Product

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['product', 'quantity']


        from django import forms


class EggProductionForm(forms.ModelForm):
    class Meta:
        model = EggProduction
        fields = [
            'chicken',
            'date_laid',
            'number_of_eggs',
            'quality',
            'weight',
            'notes',
        ]
        widgets = {
            'date_laid': forms.DateInput(attrs={'type': 'date'}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }


class IncubationForm(forms.ModelForm):
    class Meta:
        model = Incubation
        fields = [
            'chicken',
            'eggs',
            'start_date',
            'expected_hatch_date',
            'actual_hatch_date',
            'temperature',
            'humidity',
            'status',
            'notes',
            
        ]
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'expected_hatch_date': forms.DateInput(attrs={'type': 'date'}),
            'actual_hatch_date': forms.DateInput(attrs={'type': 'date'}),
            'notes': forms.Textarea(attrs={'rows': 3}),
            'eggs': forms.CheckboxSelectMultiple(),
        }


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'name',
            'category',
        ]


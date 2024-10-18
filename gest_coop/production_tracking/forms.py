# production_tracking/forms.py

from django import forms
from .models import ProductionTracking

class ProductionTrackingForm(forms.ModelForm):
    class Meta:
        model = ProductionTracking
        fields = [
            'region',
            'province',
            'type_culture',
            'date_prevue_semer',
            'date_mise_engrais',
            'quantite_engrais',
            'date_recolte',
            'notes',
        ]
        widgets = {
            'date_prevue_semer': forms.DateInput(attrs={'type': 'date'}),
            'date_mise_engrais': forms.DateInput(attrs={'type': 'date'}),
            'date_recolte': forms.DateInput(attrs={'type': 'date'}),
            'notes': forms.Textarea(attrs={'rows': 4}),
        }

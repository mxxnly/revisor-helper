from django import forms
from .models import Rating

class RatingForm(forms.ModelForm):

    class Meta:
        model = Rating
        fields = [ 'personal', 'purity', 'sorting']
        widgets = {
            'personal': forms.NumberInput(attrs={'type': 'range', 'min': '1', 'max': '100', 'step': '1', 'class': 'slider'}),
            'purity': forms.NumberInput(attrs={'type': 'range', 'min': '1', 'max': '100', 'step': '1', 'class': 'slider'}),
            'sorting': forms.NumberInput(attrs={'type': 'range', 'min': '1', 'max': '100', 'step': '1', 'class': 'slider'}),
        }

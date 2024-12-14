from django import forms
from .models import bonus_hours

class BonusForm(forms.ModelForm):
    class Meta:
        model = bonus_hours
        fields = ['user', 'month', 'year', 'hours']
        widgets = {
            'month': forms.NumberInput(attrs={'min': 1, 'max': 12, 'placeholder': 'Місяць (1-12)'}),
            'year': forms.NumberInput(attrs={'min': 2000, 'max': 2100, 'placeholder': 'Рік'}),
            'hours': forms.NumberInput(attrs={'step': 0.25, 'placeholder': 'Кількість годин'}),
        }
        labels = {
            'user': ('Користувач'),
            'month':('Місяць'),
            'year':('Рік'),
            'hours':('Години з минулого місяця'),
        }
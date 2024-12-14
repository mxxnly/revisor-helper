from django import forms
from .models import WorkLog
from main.models import Revisor
class WorkLogForm(forms.ModelForm):
    class Meta:
        model = WorkLog
        fields = ['date', 'hours_worked']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'hours_worked': forms.NumberInput(attrs={'step': '0.25'}),
        }


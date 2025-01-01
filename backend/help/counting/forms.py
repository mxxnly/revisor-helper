from django import forms
from .models import WorkLog

class WorkLogForm(forms.ModelForm):
    class Meta:
        model = WorkLog
        fields = ['date', 'hours_worked', 'minutes_worked']
        widgets = {
            'date': forms.DateInput(attrs={
                'type': 'date',
                'placeholder': 'Оберіть дату',
                'class': 'form-control',
                'aria-label': 'Дата',
            }),
            'hours_worked': forms.NumberInput(attrs={
                'step': '1',
                'placeholder': 'Вкажіть кількість годин',
                'class': 'form-control',
                'aria-label': 'Кількість годин',
            }),
            'minutes_worked': forms.NumberInput(attrs={
                'step': '1',
                'placeholder': 'Вкажіть кількість хвилин',
                'class': 'form-control',
                'aria-label': 'Кількість хвилин',
            }),
        }
        labels = {
            'date': 'Дата',
            'hours_worked': 'Години роботи',
            'minutes_worked': 'Хвилини роботи',
        }
        help_texts = {
            'date': 'Оберіть дату роботи.',
            'hours_worked': 'Вкажіть кількість годин, які ви працювали.',
            'minutes_worked': 'Вкажіть кількість хвилин, які ви працювали.',
        }

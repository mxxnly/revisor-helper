from django import forms
from .models import bonus_hours

class BonusForm(forms.ModelForm):
    class Meta:
        model = bonus_hours
        fields = ['user', 'month', 'year', 'hours', 'minutes']
        widgets = {
            'month': forms.NumberInput(attrs={
                'min': 1,
                'max': 12,
                'placeholder': 'Місяць (1-12)',
                'class': 'form-control',
            }),
            'year': forms.NumberInput(attrs={
                'min': 2000,
                'max': 2100,
                'placeholder': 'Рік',
                'class': 'form-control',
            }),
            'hours': forms.NumberInput(attrs={
                'step': 1,
                'placeholder': 'Кількість годин',
                'class': 'form-control',
            }),
            'minutes': forms.NumberInput(attrs={
                'min': 0,
                'max': 59,
                'placeholder': 'Кількість хвилин',
                'class': 'form-control',
            }),
        }
        labels = {
            'user': 'Користувач',
            'month': 'Місяць',
            'year': 'Рік',
            'hours': 'Години з минулого місяця',
            'minutes': 'Хвилини',
        }
        help_texts = {
            'user': 'Оберіть користувача, до якого застосовуються бонусні години.',
            'month': 'Вкажіть місяць (1-12).',
            'year': 'Вкажіть рік (наприклад, 2024).',
            'hours': 'Вкажіть бонусні години у форматі десяткових чисел (наприклад, 1.25).',
            'minutes': 'Вкажіть бонусні хвилини (0-59).',
        }

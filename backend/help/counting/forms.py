from django import forms
from .models import WorkLog, MoneyLog
from hours_bonus.models import bonus_hours


class MoneyForm(forms.ModelForm):
    class Meta:
        model = MoneyLog
        fields = ['date', 'money_spend']
    
        widgets = {
            'date': forms.DateInput(attrs={
                'type': 'date',
                'placeholder': 'Оберіть дату',
                'class': 'form-control date-picker',
                'aria-label': 'Дата',
            }),
            'money_spend': forms.NumberInput(attrs={
                'step': '1',
                'placeholder': 'Вкажіть гроші',
                'class': 'form-control',
                'aria-label': 'Кількість грошей, які потратили',
            }),
        }

        labels = {
            'date': 'Дата',
            'money_spend': 'Грошей потрачено'
        }
    
class WorkLogForm(forms.ModelForm):
    class Meta:
        model = WorkLog
        fields = ['date', 'hours_worked', 'minutes_worked','was_on_far_point']
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
        
    def clean_hours_worked(self):
        hours = self.cleaned_data['hours_worked']
        if hours < 0 or hours > 24:
            raise forms.ValidationError('Кількість годин повинна бути в межах від 0 до 24.')
        return hours

    def clean_minutes_worked(self):
        minutes = self.cleaned_data['minutes_worked']
        if minutes < 0 or minutes >= 60:
            raise forms.ValidationError('Кількість хвилин повинна бути в межах від 0 до 59.')
        return minutes



class BonusForm(forms.ModelForm):
    class Meta:
        model = bonus_hours
        fields = ['month', 'year', 'hours', 'minutes']
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
            'month': 'Місяць',
            'year': 'Рік',
            'hours': 'Години з минулого місяця',
            'minutes': 'Хвилини',
        }
        help_texts = {
            'month': 'Вкажіть місяць (1-12).',
            'year': 'Вкажіть рік (наприклад, 2024).',
            'hours': 'Вкажіть бонусні години у форматі десяткових чисел (наприклад, 1.25).',
            'minutes': 'Вкажіть бонусні хвилини (0-59).',
        }
    def save(self, commit=True, user=None):
        """
        Override save method to assign the logged-in user.
        """
        instance = super().save(commit=False)
        if user is not None:
            instance.user = user
        if commit:
            instance.save()
        return instance
    
    

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


class UpdatePlusMinusForm(forms.Form):
    revisor = forms.ModelChoiceField(
        queryset=Revisor.objects.all(),
        to_field_name='email',
        empty_label=None,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Ревізор'
    )
    hours_difference = forms.DecimalField(
        max_digits=5,
        decimal_places=2,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Введіть різницю годин'}),
        label='Різниця годин'
    )

    def clean_revisor(self):
        email = self.cleaned_data.get('revisor')
        if not Revisor.objects.filter(email=email).exists():
            raise forms.ValidationError("Оберіть коректного ревізора.")
        return email
    
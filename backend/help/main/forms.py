from django import forms
from main.models import Revisor

class RevisorForm(forms.ModelForm):
    date_hired = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}) 
    )
    class Meta:
        model = Revisor
        fields = ['firstname', 'lastname', 'email', 'phone_number', 'date_hired']

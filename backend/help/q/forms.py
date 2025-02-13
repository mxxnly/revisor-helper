from django import forms
from main.models import Shop

class ShopForm(forms.ModelForm):
    class Meta:
        model = Shop
        fields = ['name', 'status', 'address']
        
        labels = {
            'name': "Назва магазину",
            'status': 'Статус',
            'address':'Розташування',
        }

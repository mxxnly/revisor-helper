from django import forms
from main.models import Revisor, Shop
from main.models import Photo, Video

class RevisorForm(forms.ModelForm):
    date_hired = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'placeholder': 'Дата прийому на роботу'}),
        label="Дата прийому"
    )
    class Meta:
        model = Revisor
        fields = ['firstname', 'lastname', 'email', 'phone_number', 'date_hired']
        
        labels = {
            'firstname': "Ім'я",
            'lastname': 'Прізвище',
            'email':'Електрона пошта',
            'phone_number':'Номер телефону',
            'date_hired':'Дата прийому',
        }

class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ['image']

class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['video_file']
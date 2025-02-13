from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

class AddUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'groups', 'password1', 'password2']
        
        labels = {
            'username': "Введіть нікнейм",
            'groups': 'Групи доступу',
            'email':'Електрона пошта',
            'password1':'Пароль',
            'password2':'Підтвердіть пароль',
        }
    password1 = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    password2 = forms.CharField(
        label='Підтвердіть пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.help_text = ''

class LoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username', 'password']
        
    username = forms.CharField(
        label='Нікнейм',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )


class ProfilePictureForm(forms.Form):
    profile_picture = forms.ImageField()

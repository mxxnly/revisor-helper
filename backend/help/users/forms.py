from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

class AddUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'groups', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.help_text = ''

class LoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username', 'password']


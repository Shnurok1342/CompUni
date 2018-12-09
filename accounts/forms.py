from django import forms
from .models import UserProfile

class LoginForm(forms.Form):
    username = forms.CharField(label = "Имя")
    password = forms.CharField(widget = forms.PasswordInput, label = "Пароль")

from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User


class UserRegisterForm(UserCreationForm):
    """Form for user registration."""
    email = forms.EmailField(required=True)
    role = forms.ChoiceField(choices=[
        ('customer', 'Customer'),
        ('staff', 'Staff'),
        ('admin', 'Admin'),
    ], initial='customer')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'role')


class UserLoginForm(forms.Form):
    """Form for user login."""
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)

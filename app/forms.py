from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Food


class RegisterForm(UserCreationForm):       #UserCreationForm is a built-in Django form used for user registration.
    email = forms.EmailField()

    class Meta:         #Which model this form is connected to and which fields to use.
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class FoodForm(forms.ModelForm):
    class Meta:
        model = Food
        fields = '__all__'




# form.is_valid()-->checks:
# Empty fields
# Invalid numbers
# Invalid emails
# Custom rules

# Less Code


# Easy Database Saving


# Generate HTML Automatically


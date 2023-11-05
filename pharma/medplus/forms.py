# forms.py

from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from .models import Prescription, ShippingAddress


# create user registration form
class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        labels = {
            'username': 'UserName',
            'email': 'Email',
            'password1': 'Password',
            'password2': 'Confirm Password',

        }


# create prescription form
class PrescriptionForm(forms.ModelForm):
    class Meta:
        model = Prescription
        fields = ['patient_name', 'image']


# create  shipping address form
class ShippingAddressForm(forms.ModelForm):
    class Meta:
        model = ShippingAddress
        fields = ['user', 'address', 'city', 'state', 'pin_code', 'mobile']




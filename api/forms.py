from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Customer

class customerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['email', 'phone','role']

class createUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']        

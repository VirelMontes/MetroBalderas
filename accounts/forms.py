from django import forms
# from .models import User, Address

from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
# class UserForm(forms.ModelForm):
#     class Meta:
#         model = User
#         fields = ('username', 'email', 'phone_number')

# class AddressForm(forms.ModelForm):
#     class Meta:
#         model = Address
#         fields = ('line1', 'line2', 'city', 'state', 'zip_code')



class LoginForm(forms.Form):
    username = forms.CharField(max_length=65)
    password = forms.CharField(max_length=65, widget=forms.PasswordInput)
    

class RegisterForm(UserCreationForm):
    class Meta:
        model=User
        fields = ['username','email','password1','password2'] 
   

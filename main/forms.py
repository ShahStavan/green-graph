from distutils.command.upload import upload
from email.policy import default
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from . models import Stock


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        

# create class for stock form
class StockForm(forms.ModelForm):
	class Meta:
		model = Stock
		fields = ["ticker"] # python list
    
    
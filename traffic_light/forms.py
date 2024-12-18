from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django import forms
from django.forms import ModelForm
from django.forms.widgets import PasswordInput,TextInput
from . models import *

# Create a auser(Model Form)
class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

# Authenticate a user (Model Form)
class LoginForm(AuthenticationForm):
    username = forms.CharField(widget = TextInput(),max_length=10)
    password = forms.CharField(widget = PasswordInput())

class ImageForm(ModelForm):
    class Meta:
        model = UploadImg 
        fields = ['image', 'choice_field']
        labels = {
            'image': 'Select an image to test on AI model:',
            'choice_field':'Choose the type of test you want to perform:'
        }


class IncidentForm(ModelForm):
    class Meta:
        model = Incident
        fields = [ 'Date', 'Time', 'IsAccident', 'IsCongestion']



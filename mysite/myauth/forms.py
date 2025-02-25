from django.contrib.auth.models import Group
from django import forms
from django.forms import ModelForm
from django.core import validators
from .models import Profile

class ProfileForm(ModelForm):
    class Meta():
        model = Profile
        fields = ("avatar",)

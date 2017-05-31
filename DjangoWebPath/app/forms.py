"""
Definition of forms.
"""

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import ugettext_lazy as _
import re

class BootstrapAuthenticationForm(AuthenticationForm):
    """Authentication form which uses boostrap CSS."""
    username = forms.CharField(min_length=5, max_length=30,
                               widget=forms.TextInput({
                                   'class': 'form-control inp_login',
                                   'placeholder': 'User name'}))
    password = forms.CharField(min_length=8, max_length=30,
                               label=_("Password"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control inp_login',
                                   'placeholder':'Password'}))

    def clean_username(self):
        inp = self.cleaned_data['username']
        if not re.match('^[A-Za-z0-9]{5,30}$', inp):
            raise forms.ValidationError("Incorrect username (5-30 numbers and letters)")
        return inp

    def clean_password(self):
        inp = self.cleaned_data['password']
        if not re.match('^[A-Za-z0-9]{8,30}$', inp):
            raise forms.ValidationError("Incorrect password (8-30 numbers and letters)")
        return inp


class BootstrapRegistrationForm(UserCreationForm):
    """Registration form which uses boostrap CSS."""
    username = forms.CharField(min_length=5, max_length=30,
                               widget=forms.TextInput({
                                   'class': 'form-control inp_login',
                                   'placeholder': 'User name'}))

    password1 = forms.CharField(min_length=8, max_length=30,
                               label=_("Password"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control inp_login',
                                   'placeholder':'Password'}))

    password2 = forms.CharField(min_length=8, max_length=30,
                               label=_("Password Confirmation"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control inp_login',
                                   'placeholder':'Password'}))

    def clean_username(self):
        inp = self.cleaned_data['username']
        if not re.match('^[A-Za-z0-9]{5,30}$', inp):
            raise forms.ValidationError("Incorrect username (5-30 numbers and letters)")
        return inp

    def clean_password1(self):
        inp = self.cleaned_data['password1']
        if not re.match('^[A-Za-z0-9]{8,30}$', inp):
            raise forms.ValidationError("Incorrect password (8-30 numbers and letters)")
        return inp




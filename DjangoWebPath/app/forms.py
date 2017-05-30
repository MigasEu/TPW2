"""
Definition of forms.
"""

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _
import re

class BootstrapAuthenticationForm(AuthenticationForm):
    """Authentication form which uses boostrap CSS."""
    username = forms.CharField(min_length=3, max_length=12,
                               widget=forms.TextInput({
                                   'class': 'form-control inp_login',
                                   'placeholder': 'User name'}))
    password = forms.CharField(min_length=3, max_length=12,
                               label=_("Password"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control inp_login',
                                   'placeholder':'Password'}))

    def clean_username(self):
        inp = self.cleaned_data['username']
        if not re.match('^[A-Za-z0-9]{3,12}$', inp):
            raise forms.ValidationError("Incorrect username (3-12 numbers and letters)")
        return inp

    def clean_password(self):
        inp = self.cleaned_data['password']
        if not re.match('^[A-Za-z0-9]{3,12}$', inp):
            raise forms.ValidationError("Incorrect password (3-12 numbers and letters)")
        return inp


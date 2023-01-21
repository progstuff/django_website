from django import forms
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from ..models import UserProfile


class AuthenticateForm(forms.Form):
    email = forms.CharField(label=_('E-mail'), widget=forms.EmailInput)
    password = forms.CharField(label=_('Пароль'), widget=forms.PasswordInput)

    def get_error_messages(self):
        errors = {'email': '',
                  'password': ''}
        return errors




from django import forms
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from ..models import UserProfile


class OrderForm(forms.Form):
    full_name = forms.CharField(label=_('ФИО'))
    email = forms.CharField(label=_('E-mail'), widget=forms.EmailInput)
    phone = forms.CharField(label=_('Телефон'))

    def clean_phone_confirm(self):
        p = self.cleaned_data.get('phone', '')
        return p

    def get_error_messages(self):
        errors = {'email': '',
                  'phone': ''}

        return errors

    def save_to_db(self):
        email = self.cleaned_data.get('email', '')
        name = self.cleaned_data.get('name', '')
        password = self.cleaned_data.get('password', '')



from django import forms
from django.utils.translation import gettext_lazy as _


class RegistrationForm(forms.Form):
    name = forms.CharField(label=_('ФИО'))
    phone = forms.CharField(label=_('Телефон'))
    email = forms.CharField(label=_('E-mail'), widget=forms.EmailInput)
    password = forms.CharField(label=_('Пароль'), widget=forms.PasswordInput)
    password_confirm = forms.CharField(label=_('Подтверждение пароля'), widget=forms.PasswordInput)

from django import forms
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError


class RegistrationForm(forms.Form):
    email = forms.CharField(label=_('E-mail'), widget=forms.EmailInput)
    password = forms.CharField(label=_('Пароль'), widget=forms.PasswordInput)
    password_confirm = forms.CharField(label=_('Подтверждение пароля'), widget=forms.PasswordInput)

    def clean_password_confirm(self):
        p1 = self.cleaned_data.get('password', '')
        p2 = self.cleaned_data.get('password_confirm', '')
        if p1 != p2 and p1 != '' and p2 != '':
            raise ValidationError(_("Пароли не совпадают"))
        if p2 == '':
            raise ValidationError(_("Пароль не введен"))
        return p2

    def get_error_messages(self):
        errors = {'email': '',
                  'password': '',
                  'password_confirm': ''}
        try:
            self.clean_password_confirm()
        except ValidationError:
            if self.cleaned_data.get('password', '') != '':
                errors['password_confirm'] = 'Пароли не совпадают'

        return errors
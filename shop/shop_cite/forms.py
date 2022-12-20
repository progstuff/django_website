from django import forms
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from .models import UserProfile


class RegistrationForm(forms.Form):
    name = forms.CharField(label=_('ФИО'))
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

    def save_to_db(self):
        email = self.cleaned_data.get('email', '')
        name = self.cleaned_data.get('name', '')
        password = self.cleaned_data.get('password', '')
        user = User.objects.create_user(username=email,
                                        email=email,
                                        password=password,
                                        first_name=name)
        user_profile = UserProfile.objects.create(user=user)



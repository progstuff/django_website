from django import forms
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from ..models import UserProfile
from django.contrib.auth import authenticate, login
from django.core.files.storage import FileSystemStorage


class ProfileForm(forms.Form):
    full_name = forms.CharField(label=_('ФИО'))
    phone = forms.CharField(label=_('Телефон'))
    email = forms.CharField(label=_('E-mail'), widget=forms.EmailInput)
    password = forms.CharField(label=_('Пароль'), widget=forms.PasswordInput)
    password_confirm = forms.CharField(label=_('Подтверждение пароля'), widget=forms.PasswordInput)
    avatar = forms.ImageField(label=_('Аватар'), required=False)

    def clean_password_confirm(self):
        p1 = self.cleaned_data.get('password', '')
        p2 = self.cleaned_data.get('password_confirm', '')
        if p1 != p2 and p1 != '' and p2 != '':
            raise ValidationError(_("Пароли не совпадают"))
        if p2 == '':
            raise ValidationError(_("Пароль не введен"))
        return p2

    def clean_avatar(self):
        return self.cleaned_data.get('avatar', '')

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

    def save_to_db(self, user, request, file):
        email = self.cleaned_data.get('email', '')
        phone = self.cleaned_data.get('phone', '')
        name = self.cleaned_data.get('full_name', '')
        password = self.cleaned_data.get('password', '')
        user.username = email
        user.set_password(password)
        user.save()
        authenticate(username=email, password=password)
        login(request, user)
        #user.update(username=email)
        #user = User.objects.create_user(username=email,
        #                                email=email,
        #                                password=password,
        #                                first_name=name)
        if file is None:
            UserProfile.objects.filter(user=user).update(full_name=name,
                                                         phone=phone)
        else:
            fs = FileSystemStorage()
            # сохраняем на файловой системе
            fs.save(file.name, file)
            UserProfile.objects.filter(user=user).update(full_name=name,
                                                         phone=phone,
                                                         avatar=file)



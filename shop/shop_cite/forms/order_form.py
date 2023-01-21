from django import forms
from django.utils.translation import gettext_lazy as _
from ..models import DELIVERY_TYPE, PAYMENT_TYPE


class OrderForm(forms.Form):
    full_name = forms.CharField(label=_('ФИО'))
    email = forms.CharField(label=_('E-mail'), widget=forms.EmailInput)
    phone = forms.CharField(label=_('Телефон'))
    delivery_type = forms.ChoiceField(widget=forms.RadioSelect,
                                      choices=DELIVERY_TYPE)
    town = forms.CharField(label=_('Город'))
    address = forms.CharField(label=_('Адрес'))
    payment_type = forms.ChoiceField(widget=forms.RadioSelect,
                                     choices=PAYMENT_TYPE)


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



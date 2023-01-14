from django import forms
from django.utils.translation import gettext_lazy as _


class PaymentForm(forms.Form):
    card_number = forms.CharField(label=_('Card_number'))

    def get_error_messages(self):
        errors = {'card_number': ''}
        return errors




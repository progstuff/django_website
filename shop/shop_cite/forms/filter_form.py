from django import forms
from django.utils.translation import gettext_lazy as _


class FilterForm(forms.Form):
    querry = forms.CharField(label=_('Название'))
    price = forms.CharField(label=_('Цена'))




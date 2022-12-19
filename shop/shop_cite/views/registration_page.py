from .view_utils import BaseTemplate
from ..forms import RegistrationForm
from django.core.exceptions import ValidationError


class RegistrationPage(BaseTemplate):

    def get(self, request):
        form = RegistrationForm()
        return self.get_render(request,
                               'shop_cite/registration.html',
                               context={'form': form})

    def post(self, request):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            return self.get_render(request,
                                   'shop_cite/index.html',
                                   context={'form': form, 'errors': ''})
        else:
            errors = form.get_error_messages()

            return self.get_render(request,
                                   'shop_cite/registration.html',
                                   context={'form': form, 'errors': errors})

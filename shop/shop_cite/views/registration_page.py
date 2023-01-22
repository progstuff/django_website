from .view_utils import BaseTemplate
from ..forms.registration_form import RegistrationForm
from django.db.utils import IntegrityError
from django.http import HttpResponseRedirect


class RegistrationPage(BaseTemplate):

    def get(self, request):
        form = RegistrationForm()
        return self.get_render(request,
                               'shop_cite/registration.html',
                               context={'form': form})

    def post(self, request):
        srch_page = super().post(request)
        if srch_page is None:
            form = RegistrationForm(request.POST)
            if form.is_valid():
                try:
                    form.save_to_db()
                    return HttpResponseRedirect('/')

                except IntegrityError:
                    errors = form.get_error_messages()
                    errors['email'] = 'Пользователь с таким email уже зарегистрирован'
                    return self.get_render(request,
                                           'shop_cite/registration.html',
                                           context={'form': form, 'errors': errors})
            else:
                errors = form.get_error_messages()
                return self.get_render(request,
                                       'shop_cite/registration.html',
                                       context={'form': form, 'errors': errors})
        return srch_page

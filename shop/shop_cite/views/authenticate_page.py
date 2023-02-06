from .view_utils import BaseTemplate
from ..forms.authenticate_form import AuthenticateForm
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.views.generic import View


class AuthenticatePage(BaseTemplate):

    def get(self, request):
        form = AuthenticateForm()
        return self.get_render(request,
                               'shop_cite/authenticate.html',
                               context={'form': form, 'errors': ''})

    def post(self, request):
        srch_page = super().post(request)
        if srch_page is None:
            form = AuthenticateForm(request.POST)
            if form.is_valid():
                username = form.cleaned_data['email']
                password = form.cleaned_data['password']
                user = authenticate(username=username, password=password)
                errors = form.get_error_messages()
                if user:
                    if user.is_active:
                        login(request, user)
                        return HttpResponseRedirect('/')
                    else:
                        errors['email'] = 'Учётная запись не активна'
                else:
                    errors['password'] = 'Ошибка в логине или пароле'
            return self.get_render(request,
                                   'shop_cite/authenticate.html',
                                   context={'form': form, 'errors': errors})
        return srch_page


class LogOutView(View):

    def get(self, request):
        user = request.user
        if not user.is_anonymous:
            logout(request)
        return HttpResponseRedirect('/')

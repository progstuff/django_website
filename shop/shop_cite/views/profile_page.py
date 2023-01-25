from .view_utils import BaseTemplate
from ..forms.profile_form import ProfileForm
from ..models import UserProfile
from django.http import HttpResponseRedirect
from django.db.utils import IntegrityError


class ProfilePage(BaseTemplate):

    def get(self, request):
        user = request.user
        if not user.is_anonymous:
            user_profile = UserProfile.objects.get(user=user)
            form = ProfileForm(initial={'full_name': user_profile.full_name,
                                        'email': user.username,
                                        'phone': user_profile.phone})

            return self.get_render(request,
                                   'shop_cite/profile.html',
                                   context={'form': form})
        else:
            return HttpResponseRedirect('/')

    def post(self, request):
        user = request.user
        if not user.is_anonymous:
            srch_page = super().post(request)
            if srch_page is None:
                form = ProfileForm(request.POST)
                if form.is_valid():
                    try:
                        form.save_to_db(request.user, request)
                        a = 1
                        return HttpResponseRedirect('/account')

                    except IntegrityError:
                        pass
                        #errors = form.get_error_messages()
                        #errors['email'] = 'Пользователь с таким email уже зарегистрирован'
                        #return self.get_render(request,
                        #                       'shop_cite/registration.html',
                        #                       context={'form': form, 'errors': errors})
                else:
                    errors = form.get_error_messages()
                    return self.get_render(request,
                                           'shop_cite/profile.html',
                                           context={'form': form, 'errors': errors})
            return srch_page
        return HttpResponseRedirect('/')

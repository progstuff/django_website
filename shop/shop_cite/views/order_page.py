from .view_utils import BaseTemplate
from ..models import UserProfile
from django.contrib.auth.models import User
from ..forms.order_form import OrderForm
from django.shortcuts import redirect
from django.urls import reverse


class OrderPage(BaseTemplate):

    def get(self, request):
        user = request.user
        user_profile = UserProfile.objects.filter(user=user)
        if len(user_profile) == 1:
            user_profile = user_profile[0]
            form = OrderForm(initial={'full_name': user_profile.full_name,
                                      'email': user.username,
                                      'phone': user_profile.phone,
                                      'town': '',
                                      'address': ''})
        return self.get_render(request,
                               'shop_cite/order.html',
                               context={'form': form})

    def post(self, request):
        form = OrderForm(request.POST)
        if form.is_valid():
            return self.get_render(request,
                                   'shop_cite/order.html',
                                   context={'form': form,
                                            'is_ok': True})
        else:
            return self.get_render(request,
                                   'shop_cite/order.html',
                                   context={'form': form,
                                            'is_ok': False})

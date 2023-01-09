from .view_utils import BaseTemplate
from ..models import UserProfile
from django.contrib.auth.models import User
from ..forms.order_form import OrderForm


class OrderPage(BaseTemplate):

    def get(self, request):
        user = request.user
        user_profile = UserProfile.objects.filter(user=user)
        if len(user_profile) == 1:
            user_profile = user_profile[0]
            form = OrderForm(initial={'full_name': user_profile.full_name,
                                      'email': user.username,
                                      'phone': user_profile.phone})
            a = 1
        return self.get_render(request,
                               'shop_cite/order.html',
                               context={'form': form})

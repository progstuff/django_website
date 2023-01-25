from .view_utils import BaseTemplate
from ..models import UserProfile, Purchase
from ..models import PAYMENT_STATE, DELIVERY_TYPE, PAYMENT_TYPE
from django.http import HttpResponseRedirect


class AccountPage(BaseTemplate):

    def get(self, request):
        user = request.user
        if not user.is_anonymous:
            user_profile = UserProfile.objects.get(user=user)
            try:
                last_purchase = Purchase.objects.filter(user_profile=user_profile).order_by('-purchase_date')[0]
                last_purchase.payment_method = self.get_long_name(last_purchase.payment_method, PAYMENT_TYPE)
                last_purchase.delivery_type = self.get_long_name(last_purchase.delivery_type, DELIVERY_TYPE)
                last_purchase.payment_state = self.get_long_name(last_purchase.payment_state, PAYMENT_STATE)
            except IndexError:
                last_purchase = None

            return self.get_render(request,
                                   'shop_cite/account.html',
                                   context={'last_order': last_purchase,
                                            'user_profile': user_profile})
        else:
            return HttpResponseRedirect('/')

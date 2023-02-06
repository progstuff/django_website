from .view_utils import BaseTemplate
from ..models import UserProfile, Purchase, ProductPurchased
from django.http import HttpResponseRedirect
from ..models import PAYMENT_STATE, DELIVERY_TYPE, PAYMENT_TYPE


class OrderDetailsPage(BaseTemplate):

    def get(self, request, order_id):
        user = request.user
        if not user.is_anonymous:
            user_profile = UserProfile.objects.get(user=user)
            purchase = Purchase.objects.get(user_profile=user_profile,
                                            id=order_id)
            purchased_products = list(ProductPurchased.objects.filter(purchase=purchase))
            payment_method = self.get_long_name(purchase.payment_method, PAYMENT_TYPE)
            delivery_type = self.get_long_name(purchase.delivery_type, DELIVERY_TYPE)
            payment_state = self.get_long_name(purchase.payment_state, PAYMENT_STATE)
            return self.get_render(request,
                                   'shop_cite/order_details.html',
                                   context={'purchased_products': purchased_products,
                                            'order': purchase,
                                            'user_profile': user_profile,
                                            'delivery_type': delivery_type,
                                            'payment_method': payment_method,
                                            'payment_state': payment_state})
        else:
            return HttpResponseRedirect('/')

    def post(self, request, order_id):
        srch_page = super().post(request)
        if srch_page is None:
            return HttpResponseRedirect('/payment/{}'.format(order_id))
        return srch_page

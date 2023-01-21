from .view_utils import BaseTemplate
from ..models import UserProfile, Purchase, ProductPurchased
from django.http import HttpResponseRedirect


class OrderDetailsPage(BaseTemplate):

    def get(self, request, order_id):
        user = request.user
        if not user.is_anonymous:
            user_profile = UserProfile.objects.get(user=user)
            purchase = Purchase.objects.get(user_profile=user_profile,
                                            id=order_id)
            purchased_products = list(ProductPurchased.objects.filter(purchase=purchase))
            return self.get_render(request,
                                   'shop_cite/order_details.html',
                                   context={'purchased_products': purchased_products,
                                            'order': purchase,
                                            'user_profile': user_profile})
        else:
            return HttpResponseRedirect('/')

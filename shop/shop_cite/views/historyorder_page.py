from .view_utils import BaseTemplate
from ..models import Purchase, UserProfile
from ..models import PAYMENT_STATE, DELIVERY_TYPE, PAYMENT_TYPE


class HistoryorderPage(BaseTemplate):

    def get(self, request):
        user = request.user
        if not user.is_anonymous:
            user_profile = UserProfile.objects.get(user=user)
            orders = list(Purchase.objects.filter(user_profile=user_profile).order_by('-purchase_date'))
            for order in orders:
                order.payment_method = self.get_long_name(order.payment_method, PAYMENT_TYPE)
                order.delivery_type = self.get_long_name(order.delivery_type, DELIVERY_TYPE)
                order.payment_state = self.get_long_name(order.payment_state, PAYMENT_STATE)

        return self.get_render(request,
                               'shop_cite/historyorder.html',
                               context={'orders': orders})

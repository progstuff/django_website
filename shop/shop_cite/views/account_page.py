from .view_utils import BaseTemplate
from ..models import UserProfile, Purchase


class AccountPage(BaseTemplate):

    def get(self, request):
        user = request.user
        if not user.is_anonymous:
            user_profile = UserProfile.objects.get(user=user)
            last_purchase = Purchase.objects.filter(user_profile=user_profile).order_by('-purchase_date')[0]
        return self.get_render(request,
                               'shop_cite/account.html',
                               context={'last_order': last_purchase})

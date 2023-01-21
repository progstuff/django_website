from .view_utils import BaseTemplate
from ..models import Purchase, UserProfile


class HistoryorderPage(BaseTemplate):

    def get(self, request):
        user = request.user
        if not user.is_anonymous:
            user_profile = UserProfile.objects.get(user=user)
            orders = list(Purchase.objects.filter(user_profile=user_profile))

        return self.get_render(request,
                               'shop_cite/historyorder.html',
                               context={'orders': orders})

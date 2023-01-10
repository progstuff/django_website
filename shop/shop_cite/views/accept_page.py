from .view_utils import BaseTemplate


class AcceptOrderPage(BaseTemplate):

    def get(self, request):
        return self.get_render(request,
                               'shop_cite/accept_order.html',
                               context={})

from .view_utils import BaseTemplate


class OrderPage(BaseTemplate):

    def get(self, request):
        return self.get_render(request,
                               'shop_cite/order.html',
                               context={})

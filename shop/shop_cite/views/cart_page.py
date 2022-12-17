from .view_utils import BaseTemplate


class CartPage(BaseTemplate):

    def get(self, request):
        return self.get_render(request,
                               'shop_cite/cart.html',
                               context={})

from .view_utils import BaseTemplate


class CartPage(BaseTemplate):

    def get(self, request):
        basket = request.session.get('basket', None)
        basket_items = []
        if basket is not None:
            for product in basket:
                basket_items.append(basket[product])
        return self.get_render(request,
                               'shop_cite/cart.html',
                               context={'basket_items': basket_items})

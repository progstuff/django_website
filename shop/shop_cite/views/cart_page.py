from .view_utils import BaseTemplate


class CartPage(BaseTemplate):

    def get(self, request):
        basket = request.session.get('basket', None)
        basket_items = []
        if basket is not None:
            for product in basket:
                data = basket[product]
                data['id'] = product
                basket_items.append(data)
        return self.get_render(request,
                               'shop_cite/cart.html',
                               context={'basket_items': basket_items})

    def post(self, request):
        basket = request.session.get('basket', None)
        for key in request.POST.keys():
            if 'delete_item' in key:
                product_id = key.split('-')[1]
                del basket[product_id]
                print(product_id)
        request.session['basket'] = basket
        basket_items = []
        if basket is not None:
            for product in basket:
                data = basket[product]
                data['id'] = product
                basket_items.append(data)
        return self.get_render(request,
                               'shop_cite/cart.html',
                               context={'basket_items': basket_items})

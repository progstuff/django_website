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
                if product_id in basket:
                    del basket[product_id]
            if 'remove_item' in key:
                product_id = key.split('-')[1]
                if product_id in basket:
                    cnt = basket[product_id]['amount']
                    if cnt > 1:
                        basket[product_id]['amount'] = cnt - 1
                    else:
                        del basket[product_id]
            if 'add_item' in key:
                product_id = key.split('-')[1]
                if product_id in basket:
                    cnt = basket[product_id]['amount']
                    basket[product_id]['amount'] = cnt + 1

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

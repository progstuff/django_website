from .view_utils import BaseTemplate
from ..models import Product, ProductCharacteristics

class ProductPage(BaseTemplate):

    def get_product_data(self, pk):
        product = Product.objects.get(id=pk)
        characteristics = list(ProductCharacteristics.objects.filter(product__id=pk))
        characteristics_dict = {}
        for characteristic in characteristics:
            val = characteristics_dict.get(characteristic.group, None)
            if val == None:
                characteristics_dict[characteristic.group] = {}
            characteristics_dict[characteristic.group][characteristic.name] = characteristic.value

        description = product.description
        description_list = description.split('\n')
        params = {}
        for element in description_list:
            vals = element.split(':')
            name = vals[0]
            if len(vals) == 2:
                val = vals[1]
                if val[-1] == ';':
                    val = val[0:-1]
            else:
                val = ''
                for v in vals[1::]:
                    val += v
            params[name] = val
        return product, params, characteristics_dict

    def get(self, request, pk):
        product, params, characteristics_dict = self.get_product_data(pk)
        return self.get_render(request,
                               'shop_cite/product.html',
                               context={'product': product,
                                        'description': params,
                                        'characteristics': characteristics_dict})

    def post(self, request, pk):
        product, params, characteristics_dict = self.get_product_data(pk)
        basket = request.session.get('basket', None)
        if basket is None:
            request.session['basket'] = {}
            basket = request.session.get('basket', None)
        bpr = basket.get(str(pk), None)
        if bpr is None:
            basket[str(pk)] = {'img_src': product.add1_image_src,
                               'name': product.name,
                               'description': product.description,
                               'amount': int(request.POST['amount']),
                               'price': product.price}
        else:
            basket[str(pk)]['amount'] = int(basket[str(pk)]['amount']) + int(request.POST['amount'])
            basket[str(pk)]['price'] = product.price
        request.session['basket'] = basket

        return self.get_render(request,
                               'shop_cite/product.html',
                               context={'product': product,
                                        'description': params,
                                        'characteristics': characteristics_dict})

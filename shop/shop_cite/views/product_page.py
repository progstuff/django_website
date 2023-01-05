from .view_utils import BaseTemplate
from ..models import Product

class ProductPage(BaseTemplate):

    def get(self, request, pk):
        product = Product.objects.get(id=pk)
        description = product.description
        description_list = description.split('\n')
        params = {}
        for element in description_list:
            name, val = element.split(':')
            if val[-1] == ';':
                val = val[0:-1]
            params[name] = val
        return self.get_render(request,
                               'shop_cite/product.html',
                               context={'product': product,
                                        'description': params})

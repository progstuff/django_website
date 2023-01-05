from .view_utils import BaseTemplate
from ..models import Product, ProductCharacteristics

class ProductPage(BaseTemplate):

    def get(self, request, pk):

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
        return self.get_render(request,
                               'shop_cite/product.html',
                               context={'product': product,
                                        'description': params,
                                        'characteristics': characteristics_dict})

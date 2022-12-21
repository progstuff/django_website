from .view_utils import BaseTemplate
from ..models import Product

class ProductPage(BaseTemplate):

    def get(self, request, pk):
        product = Product.objects.get(id=pk)
        return self.get_render(request,
                               'shop_cite/product.html',
                               context={'product': product})

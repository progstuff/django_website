from .view_utils import BaseTemplate
from ..models import Product


class CatalogPage(BaseTemplate):

    def get(self, request, pk):
        products = list(Product.objects.filter(category__id=pk))
        return self.get_render(request,
                               'shop_cite/catalog.html',
                               context={'products': products})

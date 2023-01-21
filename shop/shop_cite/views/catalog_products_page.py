from .view_utils import BaseTemplate
from ..models import Product, Category


class CatalogProductsPage(BaseTemplate):

    def get(self, request, pk):
        category = Category.objects.get(id=pk)
        products = list(Product.objects.filter(category=category))
        return self.get_render(request,
                               'shop_cite/catalog_products.html',
                               context={'products': products,
                                        'category': category})

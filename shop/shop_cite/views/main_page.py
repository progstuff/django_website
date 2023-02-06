from .view_utils import BaseTemplate
from ..models import Category, Product


class MainPage(BaseTemplate):

    def get(self, request):
        popular_categories = list(Category.objects.filter(has_subcategories=False).order_by('?')[:3])
        popular_products = list(Product.objects.order_by('?')[:8])
        limited_products = list(Product.objects.order_by('?')[:8])
        return self.get_render(request,
                               'shop_cite/index.html',
                               context={'popular_categories': popular_categories,
                                        'popular_products': popular_products,
                                        'limited_products': limited_products})

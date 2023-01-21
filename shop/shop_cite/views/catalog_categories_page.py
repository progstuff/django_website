from .view_utils import BaseTemplate
from ..models import Category

class CatalogCategoriesPage(BaseTemplate):


    def get(self, request, pk):
        categories = list(Category.objects.filter(parent_category__id=pk))
        return self.get_render(request,
                               'shop_cite/catalog_categories.html',
                               context={'categories': categories,
                                        'root_category': categories[0].parent_category})

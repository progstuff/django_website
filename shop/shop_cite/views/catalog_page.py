from .view_utils import BaseTemplate


class CatalogPage(BaseTemplate):

    def get(self, request):
        return self.get_render(request,
                               'shop_cite/catalog.html',
                               context={})

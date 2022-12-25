from .view_utils import BaseTemplate


class ProductPage(BaseTemplate):

    def get(self, request):
        return self.get_render(request,
                               'shop_cite/product.html',
                               context={})

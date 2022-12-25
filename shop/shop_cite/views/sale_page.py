from .view_utils import BaseTemplate


class SalePage(BaseTemplate):

    def get(self, request):
        return self.get_render(request,
                               'shop_cite/sale.html',
                               context={})

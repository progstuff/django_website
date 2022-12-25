from .view_utils import BaseTemplate


class OrderDetailsPage(BaseTemplate):

    def get(self, request):
        return self.get_render(request,
                               'shop_cite/oneorder.html',
                               context={})

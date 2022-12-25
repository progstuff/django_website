from .view_utils import BaseTemplate


class MainPage(BaseTemplate):

    def get(self, request):
        return self.get_render(request,
                               'shop_cite/index.html',
                               context={})

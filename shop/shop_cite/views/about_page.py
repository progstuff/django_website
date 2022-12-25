from .view_utils import BaseTemplate


class AboutPage(BaseTemplate):

    def get(self, request):
        return self.get_render(request,
                               'shop_cite/about.html',
                                context={})

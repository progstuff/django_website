from .view_utils import BaseTemplate


class HistoryorderPage(BaseTemplate):

    def get(self, request):
        return self.get_render(request,
                               'shop_cite/historyorder.html',
                               context={})

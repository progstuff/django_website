from .view_utils import BaseTemplate


class ProgressPaymentPage(BaseTemplate):

    def get(self, request):
        return self.get_render(request,
                               'shop_cite/progressPayment.html',
                               context={})

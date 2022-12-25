from .view_utils import BaseTemplate


class PaymentPage(BaseTemplate):

    def get(self, request):
        return self.get_render(request,
                               'shop_cite/payment.html',
                               context={})

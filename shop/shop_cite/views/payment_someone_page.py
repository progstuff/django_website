from .view_utils import BaseTemplate


class PaymentSomeonePage(BaseTemplate):

    def get(self, request):
        return self.get_render(request,
                               'shop_cite/paymentsomeone.html',
                               context={})

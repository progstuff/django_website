from .view_utils import BaseTemplate
from ..models import Purchase
from ..forms.payment_form import PaymentForm


class PaymentPage(BaseTemplate):

    def get(self, request, order_id):
        purchase = Purchase.objects.get(id=order_id)
        form = PaymentForm()
        if purchase.payment_state == 'Н':
            return self.get_render(request,
                                   'shop_cite/payment.html',
                                   context={'form': form,
                                            'is_random': purchase.payment_method == 'Н'})
        else:
            return self.get_render(request,
                                   'shop_cite/progressPayment.html',
                                   context={'order_id': order_id,
                                            'not_payed': False})

    def post(self, request, order_id):

        purchase = Purchase.objects.get(id=order_id)
        if purchase.payment_state == 'Н':
            form = PaymentForm(request.POST)
            if form.is_valid():
                purchase.payment_state = 'О'
                purchase.save()
                return self.get_render(request,
                                       'shop_cite/progressPayment.html',
                                       context={'form': form,
                                                'order_id': order_id,
                                                'not_payed': True})
            else:
                return self.get_render(request,
                                       'shop_cite/payment.html',
                                       context={'form': form,
                                                'order_id': order_id,
                                                'is_random': purchase.payment_method == 'Н'})
        else:
            return self.get_render(request,
                                   'shop_cite/progressPayment.html',
                                   context={'order_id': order_id,
                                            'not_payed': False})
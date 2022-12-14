from django.shortcuts import render
from django.views.generic import View


class ProgressPaymentPage(View):

    def get(self, request):
        return render(request,
                      'shop_cite/progressPayment.html',
                      context={})

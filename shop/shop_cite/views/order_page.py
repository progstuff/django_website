from django.shortcuts import render
from django.views.generic import View


class OrderPage(View):

    def get(self, request):
        return render(request,
                      'shop_cite/order.html',
                      context={})

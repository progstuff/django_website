from django.shortcuts import render
from django.views.generic import View


class CartPage(View):

    def get(self, request):
        return render(request,
                      'shop_cite/cart.html',
                      context={})

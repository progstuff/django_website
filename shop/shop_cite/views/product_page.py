from django.shortcuts import render
from django.views.generic import View


class ProductPage(View):

    def get(self, request):
        return render(request,
                      'shop_cite/product.html',
                      context={})

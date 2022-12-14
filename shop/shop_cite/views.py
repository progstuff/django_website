from django.shortcuts import render
from django.views.generic import View


class MainPage(View):

    def get(self, request):
        return render(request,
                      'shop_cite/sale.html',
                      context={})

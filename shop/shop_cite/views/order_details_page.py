from django.shortcuts import render
from django.views.generic import View


class OrderDetailsPage(View):

    def get(self, request):
        return render(request,
                      'shop_cite/oneorder.html',
                      context={})

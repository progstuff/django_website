from django.shortcuts import render
from django.views.generic import View


class CatalogPage(View):

    def get(self, request):
        return render(request,
                      'shop_cite/catalog.html',
                      context={})

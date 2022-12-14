from django.shortcuts import render
from django.views.generic import View


class AboutPage(View):

    def get(self, request):
        return render(request,
                      'shop_cite/about.html',
                      context={})

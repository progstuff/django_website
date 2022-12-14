from django.shortcuts import render
from django.views.generic import View


class HistoryorderPage(View):

    def get(self, request):
        return render(request,
                      'shop_cite/historyorder.html',
                      context={})

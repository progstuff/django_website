from django.shortcuts import render
from django.views.generic import View


class ProfileAvatarPage(View):

    def get(self, request):
        return render(request,
                      'shop_cite/profileAvatar.html',
                      context={})

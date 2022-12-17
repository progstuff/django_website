from .view_utils import BaseTemplate


class ProfilePage(BaseTemplate):

    def get(self, request):
        return self.get_render(request,
                               'shop_cite/profile.html',
                               context={})

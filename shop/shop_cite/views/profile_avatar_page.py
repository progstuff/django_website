from .view_utils import BaseTemplate


class ProfileAvatarPage(BaseTemplate):

    def get(self, request):
        return self.get_render(request,
                               'shop_cite/profileAvatar.html',
                               context={})

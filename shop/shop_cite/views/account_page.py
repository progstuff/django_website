from .view_utils import BaseTemplate


class AccountPage(BaseTemplate):

    def get(self, request):
        return self.get_render(request,
                               'shop_cite/account.html',
                               context={})

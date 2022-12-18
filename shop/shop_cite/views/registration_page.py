from .view_utils import BaseTemplate
from ..forms import RegistrationForm


class RegistrationPage(BaseTemplate):

    def get(self, request):
        form = RegistrationForm()
        a = form.visible_fields()
        b = 1
        return self.get_render(request,
                               'shop_cite/registration.html',
                               context={'form': form})

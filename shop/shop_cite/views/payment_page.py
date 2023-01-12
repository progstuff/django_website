from .view_utils import BaseTemplate


class PaymentPage(BaseTemplate):

    def get(self, request):
        user = request.user
        #user_profile = UserProfile.objects.filter(user=user)

        return self.get_render(request,
                               'shop_cite/payment.html',
                               context={})

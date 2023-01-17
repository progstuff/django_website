from .view_utils import BaseTemplate
from ..models import UserProfile, Purchase, ProductPurchased, Product
from ..forms.order_form import OrderForm
from django.http import HttpResponseRedirect


class OrderPage(BaseTemplate):

    def get(self, request):
        user = request.user
        user_profile = UserProfile.objects.filter(user=user)
        if len(user_profile) == 1:
            user_profile = user_profile[0]
            form = OrderForm(initial={'full_name': user.first_name,
                                      'email': user.username,
                                      'phone': user_profile.phone,
                                      'town': user_profile.town,
                                      'address': user_profile.address})
        return self.get_render(request,
                               'shop_cite/order.html',
                               context={'form': form,
                                        'is_ok': False,
                                        'basket_items': []})

    def post(self, request):
        if request.POST.get('check_data', None) is not None:
            form = OrderForm(request.POST)
            basket = request.session.get('basket', None)
            basket_items = []
            # get products from basket to template
            if basket is not None:
                for product in basket:
                    data = basket[product]
                    data['id'] = product
                    basket_items.append(data)
            if form.is_valid():
                # confirm order

                # save user_profile data to db
                user = request.user
                user_profile = UserProfile.objects.get(user=user)
                user_profile.town = form.cleaned_data['town']
                user_profile.full_name = form.cleaned_data['full_name']
                user_profile.phone = form.cleaned_data['phone']
                user_profile.address = form.cleaned_data['address']
                user_profile.payment_method = form.cleaned_data['payment_type']
                user_profile.delivery_type = form.cleaned_data['delivery_type']
                user_profile.save()
                ################################

                return self.get_render(request,
                                       'shop_cite/order.html',
                                       context={'form': form,
                                                'is_ok': True,
                                                'basket_items': basket_items})
            else:
                # fill form again
                return self.get_render(request,
                                       'shop_cite/order.html',
                                       context={'form': form,
                                                'is_ok': False,
                                                'basket_items': basket_items})
        else:
            # redirect to payment

            # save order to db######################################################
            user = request.user
            user_profile = UserProfile.objects.get(user=user)
            cnt, total_sum = self.get_basket_items_cnt(request)
            purchase = Purchase.objects.create(user_profile=user_profile,
                                               total_sum=total_sum,
                                               payment_method=user_profile.payment_method,
                                               delivery_type=user_profile.delivery_type)
            #########################################################################

            basket = request.session.get('basket', None)

            # get products from basket to template
            if basket is not None:
                for product in basket:
                    data = basket[product]
                    # save order details
                    ProductPurchased.objects.create(purchase=purchase,
                                                    product=Product.objects.filter(id=int(product))[0],
                                                    price=data['price'],
                                                    amount=data['amount'])
                    ######################################################

            return HttpResponseRedirect('/payment/{}'.format(purchase.id))

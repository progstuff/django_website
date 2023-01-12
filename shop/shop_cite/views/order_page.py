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
            form = OrderForm(request.POST)
            form.is_valid()
            user = request.user
            user_profile = UserProfile.objects.filter(user=user).update(town=form.cleaned_data['town'],
                                                                        full_name=form.cleaned_data['full_name'],
                                                                        phone=form.cleaned_data['phone'],
                                                                        address=form.cleaned_data['address'],
                                                                        payment_method=form.cleaned_data['payment_type'],
                                                                        delivery_type=form.cleaned_data['delivery_type'])

            purchase = Purchase.objects.create()
            basket = request.session.get('basket', None)
            # get products from basket to template
            if basket is not None:
                for product in basket:
                    data = basket[product]
                    ProductPurchased.objects.create(purchase=purchase,
                                                    product=Product.objects.filter(id=int(product))[0],
                                                    store=None,
                                                    price=data['price'],
                                                    amount=data['amount'])
            return HttpResponseRedirect('/payment')

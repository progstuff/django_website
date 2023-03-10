from .view_utils import BaseTemplate
from ..models import Product, ProductCharacteristics, Review, UserProfile
from ..forms.review_form import ReviewForm


class ProductPage(BaseTemplate):

    def get_product_data(self, pk):
        product = Product.objects.get(id=pk)
        characteristics = list(ProductCharacteristics.objects.filter(product__id=pk))
        characteristics_dict = {}
        for characteristic in characteristics:
            val = characteristics_dict.get(characteristic.group, None)
            if val == None:
                characteristics_dict[characteristic.group] = {}
            characteristics_dict[characteristic.group][characteristic.name] = characteristic.value

        description = product.description
        description_list = description.split('\n')
        params = {}
        for element in description_list:
            vals = element.split(':')
            name = vals[0]
            if len(vals) == 2:
                val = vals[1]
                if val[-1] == ';':
                    val = val[0:-1]
            else:
                val = ''
                for v in vals[1::]:
                    val += v
            params[name] = val
        return product, params, characteristics_dict

    def get_reviews_cnt_str(self, reviews_cnt):
        if reviews_cnt == 0:
            return 'Нет отзывов'
        rez = '{} отзыв'.format(reviews_cnt)
        b = reviews_cnt % 100;
        if b >= 5 and b <= 19:
            return rez + 'ов'
        a = b % 10
        if a == 1:
            return rez
        if a >= 2 and a <= 4:
            return rez + 'a'
        return rez + 'ов'

    def get(self, request, pk):
        product, params, characteristics_dict = self.get_product_data(pk)
        reviews = list(Review.objects.filter(product__id=pk))
        user = request.user
        review_form = ReviewForm()
        return self.get_render(request,
                               'shop_cite/product.html',
                               context={'product': product,
                                        'description': params,
                                        'characteristics': characteristics_dict,
                                        'reviews': reviews,
                                        'reviews_cnt_str': self.get_reviews_cnt_str(len(reviews)),
                                        'is_authorised': not user.is_anonymous,
                                        'review_form': review_form})

    def post(self, request, pk):
        srch_page = super().post(request)
        if srch_page is None:
            product, params, characteristics_dict = self.get_product_data(pk)
            user = request.user
            review_form = ReviewForm()

            if request.POST.get('add_to_busket', None) is not None:
                basket = request.session.get('basket', None)
                if basket is None:
                    request.session['basket'] = {}
                    basket = request.session.get('basket', None)
                bpr = basket.get(str(pk), None)
                if bpr is None:
                    basket[str(pk)] = {'img_src': product.add1_image_src,
                                       'name': product.name,
                                       'description': product.description,
                                       'amount': int(request.POST['amount']),
                                       'price': product.price}
                else:
                    basket[str(pk)]['amount'] = int(basket[str(pk)]['amount']) + int(request.POST['amount'])
                    basket[str(pk)]['price'] = product.price
                request.session['basket'] = basket
                reviews = list(Review.objects.filter(product__id=pk))
            if request.POST.get('add_review', None) is not None:
                review_form = ReviewForm(request.POST)
                user_profile = UserProfile.objects.get(user=user)
                if review_form.is_valid():
                    Review.objects.create(user_profile=user_profile,
                                          product=product,
                                          description=review_form.cleaned_data['review'])
                    reviews = list(Review.objects.filter(product__id=pk))
            return self.get_render(request,
                                   'shop_cite/product.html',
                                   context={'product': product,
                                            'description': params,
                                            'characteristics': characteristics_dict,
                                            'reviews': reviews,
                                            'reviews_cnt_str': self.get_reviews_cnt_str(len(reviews)),
                                            'is_authorised': not user.is_anonymous,
                                            'review_form': review_form})
        return srch_page

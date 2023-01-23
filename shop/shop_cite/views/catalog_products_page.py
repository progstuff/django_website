from .view_utils import BaseTemplate
from ..models import Product, Category
from ..forms.filter_form import FilterForm
from django.db.models import Min, Max
from django.http import HttpResponseRedirect


class CatalogProductsPage(BaseTemplate):

    def get_products_cnt_str(self, products_cnt):
        if products_cnt == 0:
            return 'Товаров не найдено'
        rez = '{} товар'.format(products_cnt)
        b = products_cnt % 100;
        if b >= 5 and b <= 19:
            return rez + 'ов'
        a = b % 10
        if a == 1:
            return rez
        if a >= 2 and a <= 4:
            return rez + 'a'
        return rez + 'ов'

    def get(self, request, pk):
        form = FilterForm()
        search_val = request.GET.get('search', None)
        if search_val is None:
            category = Category.objects.get(id=pk)
        else:
            category = {}
        # get values from get querry or db############
        min_pr = request.GET.get('min_pr', None)
        max_pr = request.GET.get('max_pr', None)
        page_number = int(request.GET.get('p', 1))

        if min_pr is None or max_pr is None:
            if search_val is None:
                prices = Product.objects.filter(category=category).aggregate(Max('price'), Min('price'))
            else:
                prices = Product.objects.filter(name__icontains=search_val).aggregate(Max('price'), Min('price'))
            min_pr = prices['price__min']
            max_pr = prices['price__max']
        else:
            min_pr = float(min_pr)
            max_pr = float(max_pr)
        from_pr = float(request.GET.get('from_pr', min_pr))
        to_pr = float(request.GET.get('to_pr', max_pr))
        ##############################################

        ## sort vals #################################
        querry = request.GET.get('name', '')
        sort_val = request.GET.get('sort', None)
        sort_popular = 'popular_none'
        sort_price = 'price_none'
        sort_new = 'new_none'
        sort_review = 'review_none'
        popular_class = ''
        price_class = ''
        new_class = ''
        review_class = ''
        order_val = 'price'
        if sort_val is not None:
            data = sort_val.split('_')
            param = data[0]
            val = data[1]
            if param == 'price':
                if val == 'inc':
                    sort_price = 'price_inc'
                    price_class = ' Sort-sortBy_dec'
                    order_val = 'price'
                else:
                    sort_price = 'price_dec'
                    price_class = ' Sort-sortBy_inc'
                    order_val = '-price'
            elif param == 'popular':
                if val == 'inc':
                    sort_popular = 'popular_inc'
                    popular_class = ' Sort-sortBy_dec'
                else:
                    sort_popular = 'popular_dec'
                    popular_class = ' Sort-sortBy_inc'
            elif param == 'review':
                if val == 'inc':
                    sort_review = 'review_inc'
                    review_class = ' Sort-sortBy_dec'
                else:
                    sort_review = 'review_dec'
                    review_class = ' Sort-sortBy_inc'
            elif param == 'new':
                if val == 'inc':
                    sort_new = 'new_inc'
                    new_class = ' Sort-sortBy_dec'
                    order_val = 'name'
                else:
                    sort_new = 'new_dec'
                    new_class = ' Sort-sortBy_inc'
                    order_val = '-name'
        else:
            price_class = ' Sort-sortBy_inc'
            sort_price = 'price_dec'
            order_val = '-price'
        ##############################################
        if querry == '':
            if search_val is None:
                products = list(Product.objects.filter(category=category,
                                                       price__gte=from_pr,
                                                       price__lte=to_pr)
                                .order_by(order_val))
            else:
                products = list(Product.objects.filter(name__icontains=search_val,
                                                       price__gte=from_pr,
                                                       price__lte=to_pr)
                                .order_by(order_val))

        else:
            if search_val is None:
                products = list(Product.objects.filter(category=category,
                                                       price__gte=from_pr,
                                                       price__lte=to_pr,
                                                       name__icontains=querry)
                                .order_by(order_val))
            else:
                products = list(Product.objects.filter(name__icontains=search_val)
                                               .filter(price__gte=from_pr,
                                                       price__lte=to_pr,
                                                       name__icontains=querry)
                                               .order_by(order_val))

        if search_val is not None:
            if len(products) > 0:
                products_cnt_str = self.get_products_cnt_str(len(products))
                category['title'] = 'Найдено: {}'.format(products_cnt_str)
            else:
                category['title'] = 'Ничего не найдено'
        else:
            if len(products) > 0:
                products_cnt_str = self.get_products_cnt_str(len(products))
                category.title = 'найдено: {}'.format(products_cnt_str)
            else:
                category.title = 'ничего не найдено'
            category.title = category.name + ' - ' + category.title
        return self.get_render(request,
                               'shop_cite/catalog_products.html',
                               context={'products': products,
                                        'category': category,
                                        'form': form,
                                        'min_pr': str(min_pr),
                                        'max_pr': str(max_pr),
                                        'from_pr': str(from_pr),
                                        'to_pr': str(to_pr),
                                        'querry_name': querry,
                                        'sort_popular': sort_popular,
                                        'sort_price': sort_price,
                                        'sort_new': sort_new,
                                        'sort_review': sort_review,
                                        'popular_class': popular_class,
                                        'price_class': price_class,
                                        'new_class': new_class,
                                        'review_class': review_class,
                                        'is_category': search_val is None,
                                        'cur_page_number': page_number})

    def post(self, request, pk):

        srch_page = super().post(request)
        if srch_page is None:
            srch_val = request.GET.get('search', '')
            sort_val = request.GET.get('sort', '')

            page_number = int(request.GET.get('p', 1))
            for key in request.POST.keys():
                if 'page' in key:
                    page_val = key.split('_')[1]
                    if page_val == 'forward':
                        page_number += 1
                        if page_number > 3:
                            page_number = 3
                    if page_val == 'back':
                        page_number -= 1
                        if page_number < 1:
                            page_number = 1
                    break

            if 'filter' in request.POST:
                price = request.POST['price'].split(';')
                if srch_val == '':
                    prices = Product.objects.filter(category__id=pk).aggregate(Max('price'), Min('price'))
                else:
                    prices = Product.objects.filter(name__icontains=srch_val).aggregate(Max('price'), Min('price'))

                min_pr = int(prices['price__min'])
                max_pr = int(prices['price__max'])
                from_pr = price[0]
                to_pr = price[1]
                querry = request.POST['querry']
            else:
                from_pr = request.GET.get('from_pr', None)
                to_pr = request.GET.get('to_pr', None)
                min_pr = request.GET.get('min_pr', None)
                max_pr = request.GET.get('max_pr', None)
                querry = request.GET.get('name', None)
                if 'price_sort' in request.POST:
                    sort_val = request.POST['price_sort']
                elif 'popular_sort' in request.POST:
                    sort_val = request.POST['popular_sort']
                elif 'new_sort' in request.POST:
                    sort_val = request.POST['new_sort']
                elif 'review_sort' in request.POST:
                    sort_val = request.POST['review_sort']

                if sort_val != '':
                    if sort_val[-4::] != 'none':
                        if sort_val[-3::] == 'dec':
                            sort_val = sort_val[:-3] + 'inc'
                        else:
                            sort_val = sort_val[:-3] + 'dec'
                    else:
                        sort_val = sort_val[:-4] + 'dec'

            params = {}
            params['p'] = page_number
            params['search'] = srch_val
            params['name'] = querry
            params['from_pr'] = from_pr
            params['to_pr'] = to_pr
            params['min_pr'] = min_pr
            params['max_pr'] = max_pr
            params['sort'] = sort_val

            link = '/catalog-products/{0}'.format(pk)
            is_first = True
            for key, val in params.items():
                if val != '' and val is not None:
                    if is_first:
                        link += '?{0}={1}'.format(key, val)
                        is_first = False
                    else:
                        link += '&{0}={1}'.format(key, val)

            return HttpResponseRedirect(link)
        return srch_page

from .view_utils import BaseTemplate
from ..models import Product, Category
from ..forms.filter_form import FilterForm
from django.db.models import Min, Max
from django.http import HttpResponseRedirect
from ..app_settings import PAGE_SIZE, PAGE_SHIFT
from math import ceil


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

    def get_page_number(self, page_val, min_val, max_val):
        if page_val < min_val:
            res_page_number = min_val
        elif page_val > max_val:
            res_page_number = max_val
        else:
            res_page_number = page_val
        return res_page_number

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
        cur_page = int(request.GET.get('p', 1))

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
                data = Product.objects.filter(category=category,
                                              price__gte=from_pr,
                                              price__lte=to_pr)
            else:
                data = Product.objects.filter(name__icontains=search_val,
                                              price__gte=from_pr,
                                              price__lte=to_pr)
        else:
            if search_val is None:
                data = Product.objects.filter(category=category,
                                              price__gte=from_pr,
                                              price__lte=to_pr,
                                              name__icontains=querry)

            else:
                data = Product.objects.filter(name__icontains=search_val).\
                                       filter(price__gte=from_pr,
                                              price__lte=to_pr,
                                              name__icontains=querry)
        products_cnt = data.count()
        max_page = int(ceil(products_cnt/PAGE_SIZE))
        cur_page = self.get_page_number(cur_page, 1, max_page)
        prev_page = self.get_page_number(cur_page - 1, 1, max_page)
        next_page = self.get_page_number(cur_page + 1, 1, max_page)
        start_ind = (cur_page-1)*PAGE_SIZE
        end_ind = cur_page*PAGE_SIZE - 1
        if start_ind < 0:
            start_ind = 0
        if end_ind >= products_cnt:
            end_ind = products_cnt - 1
        products = list(data.order_by(order_val)[start_ind:end_ind + 1])
        if search_val is not None:
            if len(products) > 0:
                products_cnt_str = self.get_products_cnt_str(products_cnt)
                category['title'] = 'Найдено: {}'.format(products_cnt_str)
            else:
                category['title'] = 'Ничего не найдено'
        else:
            if len(products) > 0:
                products_cnt_str = self.get_products_cnt_str(products_cnt)
                category.title = 'найдено: {}'.format(products_cnt_str)
            else:
                category.title = 'ничего не найдено'
            category.title = category.name + ' - ' + category.title

        start_page = cur_page - (PAGE_SHIFT-1)
        end_page = cur_page + (PAGE_SHIFT-1)
        left_point_page = None
        right_point_page = None
        if start_page < 1:
            start_page = 1
        if end_page > max_page:
            end_page = max_page
        pages = [(x, '') for x in range(start_page, end_page + 1)]
        if start_page - 1 >= 2:
            left_point_page = start_page - 1
            pages = [(1, ''), ('...', left_point_page)] + pages
        elif start_page - 1 == 1:
            pages = [(1, '')] + pages
        if max_page - end_page >= 2:
            right_point_page = end_page + 1
            pages = pages + [('...', right_point_page), (max_page, '')]

        elif max_page - end_page == 1:
            pages = pages + [(max_page, '')]

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
                                        'max_page': max_page,
                                        'left_point_page': left_point_page,
                                        'right_point_page': right_point_page,
                                        'prev_page': prev_page,
                                        'next_page': next_page,
                                        'cur_page': cur_page,
                                        'pages': pages})

    def post(self, request, pk):
        srch_page = super().post(request)
        if srch_page is None:
            srch_val = request.GET.get('search', '')
            sort_val = request.GET.get('sort', '')
            page_number = int(request.GET.get('p', 1))

            is_page_button = False
            for key in request.POST.keys():
                if 'page' in key:
                    data = key.split('_')
                    page_val = data[1]
                    if page_val == 'forward':
                        page_number = int(data[2])
                    elif page_val == 'back':
                        page_number = int(data[2])
                    else:
                        page_number = int(page_val)
                    is_page_button = True
                    break
            if is_page_button:
                from_pr = request.GET.get('from_pr', None)
                to_pr = request.GET.get('to_pr', None)
                min_pr = request.GET.get('min_pr', None)
                max_pr = request.GET.get('max_pr', None)
                querry = request.GET.get('name', None)

            elif 'filter' in request.POST:
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

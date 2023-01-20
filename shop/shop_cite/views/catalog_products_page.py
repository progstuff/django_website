from .view_utils import BaseTemplate
from ..models import Product, Category
from ..forms.filter_form import FilterForm
from django.db.models import Min, Max
from django.http import HttpResponseRedirect


class CatalogProductsPage(BaseTemplate):

    def get(self, request, pk):
        form = FilterForm()
        category = Category.objects.get(id=pk)

        # get values from get querry or db############
        min_pr = request.GET.get('min_pr', None)
        max_pr = request.GET.get('max_pr', None)
        if min_pr is None or max_pr is None:
            prices = Product.objects.filter(category=category).aggregate(Max('price'), Min('price'))
            min_pr = prices['price__min']
            max_pr = prices['price__max']
        else:
            min_pr = float(min_pr)
            max_pr = float(max_pr)
        from_pr = float(request.GET.get('from_pr', min_pr))
        to_pr = float(request.GET.get('to_pr', max_pr))
        ##############################################

        ## sort vals #################################
        sort_val = request.GET.get('sort', None)
        sort_popular = 'popular_none'
        sort_price = 'price_none'
        sort_new = 'new_none'
        sort_review = 'review_none'
        popular_class = ''
        price_class = ''
        new_class = ''
        review_class = ''
        if sort_val is not None:
            data = sort_val.split('_')
            param = data[0]
            val = data[1]
            if param == 'price':
                if val == 'dec':
                    sort_price = 'price_inc'
                    price_class = ' Sort-sortBy_dec'
                else:
                    sort_price = 'price_inc'
                    price_class = ' Sort-sortBy_dec'
            elif param == 'popular':
                if val == 'dec':
                    sort_popular = 'popular_inc'
                    popular_class = ' Sort-sortBy_dec'
                else:
                    sort_popular = 'popular_dec'
                    popular_class = ' Sort-sortBy_inc'
            elif param == 'review':
                if val == 'dec':
                    sort_review = 'review_inc'
                    review_class = ' Sort-sortBy_dec'
                else:
                    sort_review = 'review_dec'
                    review_class = ' Sort-sortBy_inc'
            elif param == 'new':
                if val == 'dec':
                    sort_new = 'new_inc'
                    new_class = ' Sort-sortBy_inc'
                else:
                    sort_price = 'new_dec'
                    new_class = ' Sort-sortBy_dec'
        else:
            price_class = ' Sort-sortBy_inc'
            sort_price = 'price_dec'
        ##############################################

        products = list(Product.objects.filter(category=category, price__gte=from_pr, price__lte=to_pr))
        return self.get_render(request,
                               'shop_cite/catalog_products.html',
                               context={'products': products,
                                        'category': category,
                                        'form': form,
                                        'min_pr': str(min_pr),
                                        'max_pr': str(max_pr),
                                        'from_pr': str(from_pr),
                                        'to_pr': str(to_pr),
                                        'sort_popular': sort_popular,
                                        'sort_price': sort_price,
                                        'sort_new': sort_new,
                                        'sort_review': sort_review,
                                        'popular_class': popular_class,
                                        'price_class': price_class,
                                        'new_class': new_class,
                                        'review_class': review_class})

    def post(self, request, pk):
        sort_val = request.GET.get('sort', '')
        if 'filter' in request.POST:
            price = request.POST['price'].split(';')
            prices = Product.objects.filter(category__id=pk).aggregate(Max('price'), Min('price'))
            min_pr = int(prices['price__min'])
            max_pr = int(prices['price__max'])
            from_pr = price[0]
            to_pr = price[1]
        else:
            from_pr = request.GET.get('from_pr', None)
            to_pr = request.GET.get('to_pr', None)
            min_pr = request.GET.get('min_pr', None)
            max_pr = request.GET.get('max_pr', None)
        if 'price_sort' in request.POST:
            if request.POST['price_sort'][-4::] != 'none':
                sort_val = request.POST['price_sort']
        elif 'popular_sort' in request.POST:
            if request.POST['popular_sort'][-4::] != 'none':
                sort_val = request.POST['popular_sort']
        elif 'new_sort' in request.POST:
            if request.POST['new_sort'][-4::] != 'none':
                sort_val = request.POST['new_sort']
        elif 'review_sort' in request.POST:
            if request.POST['review_sort'][-4::] != 'none':
                sort_val = request.POST['review_sort']

        params = {}
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
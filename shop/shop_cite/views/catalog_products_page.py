from .view_utils import BaseTemplate
from ..models import Product, Category
from ..forms.filter_form import FilterForm
from django.http import HttpResponseRedirect


class CatalogProductsPage(BaseTemplate):

    def get(self, request, pk):
        form = FilterForm()
        category = Category.objects.get(id=pk)
        min_pr = float(request.GET.get('min_pr', 0))
        max_pr = float(request.GET.get('max_pr', 1000000))
        products = list(Product.objects.filter(category=category, price__gt=min_pr, price__lt=max_pr))
        return self.get_render(request,
                               'shop_cite/catalog_products.html',
                               context={'products': products,
                                        'category': category,
                                        'form': form,
                                        'min_pr': str(min_pr),
                                        'max_pr': str(max_pr)})

    def post(self, request, pk):
        form = FilterForm()
        category = Category.objects.get(id=pk)
        price = request.POST['price'].split(';')
        min_price = price[0]
        max_price = price[1]
        products = list(Product.objects.filter(category=category, price__gt=float(min_price), price__lt=float(max_price)))
        return self.get_render(request,
                               'shop_cite/catalog_products.html',
                               context={'products': products,
                                        'category': category,
                                        'form': form,
                                        'min_pr': min_price,
                                        'max_pr': max_price})
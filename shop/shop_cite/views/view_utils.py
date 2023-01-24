from django.shortcuts import render
from django.views.generic import View
from ..models import Category
from django.http import HttpResponseRedirect


class BaseTemplate(View):

    def get_long_name(self, short_name, names):
        for shrt_name, lng_name in names:
            if shrt_name == short_name:
                return lng_name
        return ''

    def get_basket_items_cnt(self, request):
        basket = request.session.get('basket', None)
        cnt = 0
        total_price = 0
        if basket is not None:
            for product in basket:
                cnt += int(basket[product]['amount'])
                total_price += int(basket[product]['amount']) * float(basket[product]['price'])
        return cnt, total_price

    def get_render(self, request, template_name,  context={}):

        lvl_one, lvl_two, lvl_three = self.get_categoryes_names()
        context['categories_lvl_one'] = lvl_one
        context['categories_lvl_two'] = lvl_two
        context['categories_lvl_three'] = lvl_three
        cnt, price = self.get_basket_items_cnt(request)
        context['basket_items_cnt'] = cnt
        context['basket_total_price'] = price

        return render(request,
                      template_name,
                      context=context)

    def get_categoryes_names(self):
        categories = list(Category.objects.select_related('parent_category').all())
        lvl_one = {}
        lvl_two = {}
        lvl_three = {}
        for category in categories:
            if category.parent_category is None:
                lvl_one[category.name] = (category.image_src, category.short_image_name, category.id, category.has_subcategories, [])
        for category in categories:
            if category.parent_category is not None:
                if category.parent_category.name in lvl_one:
                    lvl_one[category.parent_category.name][4].append(category.name)
                    lvl_two[category.name] = (category.image_src, category.short_image_name, category.id, category.has_subcategories, [])

        # для третьего уровня (если понадобится)
        for category in categories:
            if category.parent_category is not None:
                if category.parent_category.name in lvl_two:
                    lvl_two[category.parent_category.name][4].append(category.name)
                    lvl_three[category.name] = (category.image_src, category.short_image_name, category.id, category.has_subcategories, [])

        return lvl_one, lvl_two, lvl_three

    def post(self, request):
        if 'search' in request.POST:
            querry_text = request.POST['query_text']
            return HttpResponseRedirect('/catalog-products/0?search={}'.format(querry_text))


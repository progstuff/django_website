from django.shortcuts import render
from django.views.generic import View
from ..models import Category


class BaseTemplate(View):

    def get_render(self, request, template_name,  context={}):

        lvl_one, lvl_two, lvl_three = self.get_categoryes_names()
        context['categories_lvl_one'] = lvl_one
        context['categories_lvl_two'] = lvl_two
        context['categories_lvl_three'] = lvl_three
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
                lvl_one[category.name] = (category.image_src, category.short_image_name, [])
        for category in categories:
            if category.parent_category is not None:
                if category.parent_category.name in lvl_one:
                    lvl_one[category.parent_category.name][2].append(category.name)
                    lvl_two[category.name] = (category.image_src, category.short_image_name, [])

        # для третьего уровня (если понадобится)
        for category in categories:
            if category.parent_category is not None:
                if category.parent_category.name in lvl_two:
                    lvl_two[category.parent_category.name][2].append(category.name)
                    lvl_three[category.name] = (category.image_src, category.short_image_name, [])

        return lvl_one, lvl_two, lvl_three

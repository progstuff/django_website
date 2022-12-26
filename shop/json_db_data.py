import json
import requests
import os


def create_cat_model_object(id_val, parent_category_id, name, image_src, short_name):
    rez = {}
    rez['model'] = 'shop_cite.category'
    rez['pk'] = id_val
    rez['fields'] = {'parent_category': parent_category_id,
                     'name': name,
                     'image_src': image_src,
                     'short_image_name': short_name
                     }
    return rez


def get_main_category_id(main_categories, category_name):
    cnt = 0
    for category in main_categories:
        cnt += 1
        if category['url_name'] == category_name:
            return cnt
    return cnt


def create_main_categories_fixture():
    d = os.path.dirname(__file__)
    with open(d + '\\test_data\\main_categories_data.json', 'r', encoding='utf-8') as fp:
        data = json.load(fp)

    model_objects = []
    cnt = 0
    for val in data:
        cnt += 1
        file_content = requests.get(val['img_link'])
        print(val['url_name'])
        open(d + '\\shop_cite\\static\\shop_cite\\assets\\img\\icons\\departments\\' + val['url_name'] + '.svg', 'wb').write(file_content.content)

        model_objects.append(create_cat_model_object(id_val=cnt,
                                                     parent_category_id=None,
                                                     name=val['human_name'],
                                                     image_src='assets\\img\\icons\\departments\\' + val['url_name'] + '.svg',
                                                     short_name=val['url_name']))


    with open(d + '\\shop_cite\\fixtures\\main_categories_data_db.json', 'wb') as fp:
        data = json.dumps(model_objects, indent=4, ensure_ascii=False).encode('utf8')
        fp.write(data)


def create_other_categories_fixture():
    d = os.path.dirname(__file__)
    with open(d + '\\test_data\\main_categories_data.json', 'r', encoding='utf-8') as fp:
        main_categories = json.load(fp)


    start_id = 20
    ids = {}
    model_objects = []

    for main_category in main_categories:
        res = []
        main_category_name = main_category['url_name']
        with open(d + '\\test_data\\categories_data_{0}.json'.format(main_category_name), 'r', encoding='utf-8') as fp:
            other_categories = json.load(fp)

        main_cat_id = get_main_category_id(main_categories, main_category_name)
        ids[main_category_name] = main_cat_id
        cnt_id = start_id
        for category in other_categories:
            root_cat_id = ids.get(category['root'], -1)
            if root_cat_id == -1:
                ids[category['root']] = cnt_id
                root_cat_id = cnt_id
                cnt_id += 1
            cat_id = ids.get(category['value']['url_name'], -1)
            if cat_id == -1:
                ids[category['value']['url_name']] = cnt_id
                cat_id = cnt_id
                cnt_id += 1
            category['id'] = root_cat_id
            category['value']['id'] = cat_id
            res.append(category)

        for val in res:
            model_objects.append(create_cat_model_object(id_val=val['value']['id'],
                                                         parent_category_id=val['id'],
                                                         name=val['value']['human_name'],
                                                         image_src='assets\\img\\icons\\departments\\plug.svg',
                                                         short_name=val['value']['url_name']))
        start_id = cnt_id + 1

        print(len(model_objects), cnt_id - 20)

    with open(d + '\\shop_cite\\fixtures\\other_categories_data_db.json', 'wb') as fp:
        data = json.dumps(model_objects, indent=4, ensure_ascii=False).encode('utf8')
        fp.write(data)


create_main_categories_fixture()
create_other_categories_fixture()
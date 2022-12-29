import json
import requests
import os
from os.path import exists
import shutil


def create_cat_model_object(id_val, parent_category_id, name, image_src, short_name, is_product_page, big_image_src):
    rez = {}
    rez['model'] = 'shop_cite.category'
    rez['pk'] = id_val
    rez['fields'] = {'parent_category': parent_category_id,
                     'name': name,
                     'image_src': image_src,
                     'short_image_name': short_name,
                     'has_subcategories': not is_product_page,
                     'big_image_src': big_image_src
                     }
    return rez


def get_main_category_id(main_categories, category_name):
    cnt = 0
    for category in main_categories:
        cnt += 1
        if category['url_name'] == category_name:
            return cnt
    return cnt


def create_main_categories_model_objects(max_categories_cnt):
    d = os.path.dirname(__file__)
    with open(d + '\\test_data\\main_categories_data.json', 'r', encoding='utf-8') as fp:
        data = json.load(fp)

    model_objects = []
    cnt = 0
    for val in data:
        if cnt < max_categories_cnt:
            cnt += 1
            file_content = requests.get(val['img_link'])
            print(val['url_name'])
            open(d + '\\shop_cite\\static\\shop_cite\\assets\\img\\icons\\departments\\' + val['url_name'] + '.svg', 'wb').write(file_content.content)

            model_objects.append(create_cat_model_object(id_val=cnt,
                                                         parent_category_id=None,
                                                         name=val['human_name'],
                                                         image_src='assets\\img\\icons\\departments\\' + val['url_name'] + '.svg',
                                                         short_name=val['url_name'],
                                                         big_image_src='',
                                                         is_product_page=False))

    return model_objects


def create_other_categories_model_objects():
    d = os.path.dirname(__file__)
    with open(d + '\\test_data\\main_categories_data.json', 'r', encoding='utf-8') as fp:
        main_categories = json.load(fp)


    start_id = 20
    ids = {}
    model_objects = []
    product_pages_cnt = 0
    newpath = d + '\\test_data\\categories_images'
    if not exists(newpath):
        os.makedirs(newpath)

    for main_category in main_categories:
        res = []
        main_category_name = main_category['url_name']
        with open(d + '\\test_data\\categories_data_{0}.json'.format(main_category_name), 'r', encoding='utf-8') as fp:
            other_categories = json.load(fp)

        main_cat_id = get_main_category_id(main_categories, main_category_name)
        ids[main_category_name] = main_cat_id
        cnt_id = start_id
        for category in other_categories:
            file_name = newpath + '\\' + category['value']['url_name'] + '.jpg'
            if not exists(file_name):
                file_content = requests.get(category['value']['img_link'])
                print(category['value']['img_link'])
                open(file_name, 'wb').write(file_content.content)

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
                                                         short_name=val['value']['url_name'],
                                                         big_image_src='assets\\img\\content\\category\\' + val['value']['url_name'] + '.jpg',
                                                         is_product_page=val['value']['is_product_page']))
            if val['value']['is_product_page']:
                product_pages_cnt += 1
        start_id = cnt_id + 1

    return model_objects


def get_subcategories(root_categories, model_objects, max_cat_cnt):

    root_ids = []
    for cat in root_categories:
        root_ids.append(cat['pk'])

    result = []
    ids = {}
    for category in model_objects:
        if category['fields']['parent_category'] in root_ids:
            cnt = ids.get(category['fields']['parent_category'], 0)
            cnt += 1
            ids[category['fields']['parent_category']] = cnt
            if cnt <= max_cat_cnt:
                result.append(category)

    return result


def get_several_categories(main_categories_model_objects, model_objects, max_cat_cnt):
    cat1_model_objects = get_subcategories(main_categories_model_objects, model_objects, max_cat_cnt)
    cat2_model_objects = get_subcategories(cat1_model_objects, model_objects, max_cat_cnt)
    cat3_model_objects = get_subcategories(cat2_model_objects, model_objects, max_cat_cnt)
    result = cat1_model_objects + cat2_model_objects + cat3_model_objects
    return result


def save_fixtures(main_categories_model_objects, other_categories_model_objects):

    d = os.path.dirname(__file__)
    newpath = d + '\\test_data\\categories_images'
    content_path = d + '\\shop_cite\\static\\shop_cite\\assets\\img\\content\\category'
    if not exists(content_path):
        os.makedirs(content_path)

    for category in other_categories_model_objects:
        file_name = newpath + '\\' + category['fields']['short_image_name'] + '.jpg'
        dest_file_name = content_path + '\\' + category['fields']['short_image_name'] + '.jpg'
        if exists(file_name) and not exists(dest_file_name):
            shutil.copyfile(file_name, dest_file_name)

    with open(d + '\\shop_cite\\fixtures\\main_categories_data_db.json', 'wb') as fp:
        data = json.dumps(main_categories_model_objects, indent=4, ensure_ascii=False).encode('utf8')
        fp.write(data)

    with open(d + '\\shop_cite\\fixtures\\other_categories_data_db.json', 'wb') as fp:
        data = json.dumps(other_categories_model_objects, indent=4, ensure_ascii=False).encode('utf8')
        fp.write(data)


main_categories_model_objects = create_main_categories_model_objects(max_categories_cnt=6)
other_categories_model_objects = create_other_categories_model_objects()
several_categories = get_several_categories(main_categories_model_objects,
                                            other_categories_model_objects,
                                            max_cat_cnt=5)
save_fixtures(main_categories_model_objects, several_categories)

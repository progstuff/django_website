import json
import requests


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

with open('D:\\python_projects\\python_django_diploma\\shop\\test_data\\main_categories_data.json', 'r', encoding='utf-8') as fp:
    data = json.load(fp)

model_objects = []
cnt = 0
for val in data:
    cnt += 1
    file_content = requests.get(val['img_link'])
    print(val['url_name'])
    open('D:\\python_projects\\python_django_diploma\\shop\\shop_cite\\static\\shop_cite\\assets\\img\\icons\\departments\\' + val['url_name'] + '.svg', 'wb').write(file_content.content)

    model_objects.append(create_cat_model_object(id_val=cnt,
                                                 parent_category_id=None,
                                                 name=val['human_name'],
                                                 image_src='assets\\img\\icons\\departments\\' + val['url_name'] + '.svg',
                                                 short_name=val['url_name']))


with open('main_categories_data_db.json', 'wb') as fp:
    data = json.dumps(model_objects, indent=4, ensure_ascii=False).encode('utf8')
    fp.write(data)
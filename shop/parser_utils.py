import requests
from bs4 import BeautifulSoup
import time
import json
import random
import os


def get_header(s):
    s.headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 OPR/94.0.0.0'
    s.headers['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
    return s


def get_products_data_from_citilink(product_name, page_number):

    url = 'https://www.citilink.ru/catalog/{0}/?pf=discount.any%2Crating.any&&view_type=grid&f=discount.any%2Crating.any%2Cavailable.all&p={1}'.format(product_name,
                                                                                                                                                       page_number)
    s = requests.Session()
    s = get_header(s)
    r = s.get(url)
    print(r.status_code)
    print(url)

    soup = BeautifulSoup(r.text, 'html.parser')
    products = []
    for c in soup.find_all('div', class_='ProductCardVerticalLayout ProductCardVertical__layout'):
        image_src = c.next.next.next.next.next.next.attrs['src']
        title = c.next.contents[2].next.next.attrs['title']
        product_link = c.next.contents[2].next.next.attrs['href']
        price = c.contents[1].next.next.next.contents[1].next.next.contents[0]
        price = price.replace(" ", "")
        price = price.replace("\n", "")
        products.append({'name': title,
                         'price': price,
                         'detail_link': product_link,
                         'image_link': image_src})

    return products, soup


def is_last_page(page_soup, page_number):
    pages = page_soup.find_all('div', class_='PaginationWidget__wrapper-pagination')
    if len(pages) > 0:
        pages = pages[0]
        max_page_ind = 0
        for page_element in pages.contents:
            if len(page_element.attrs) == 3:
                page_ind = int(page_element.attrs['data-page'])
                if page_ind > max_page_ind:
                    max_page_ind = page_ind
        return max_page_ind == page_number or max_page_ind < page_number
    return True


def get_main_categories_data():
    url = 'https://www.citilink.ru'
    s = requests.Session()
    s = get_header(s)
    r = s.get(url)
    print(r.status_code)
    soup = BeautifulSoup(r.text, 'html.parser')
    main_categories = []
    for c in soup.find_all('div', class_='CatalogMenu__category-items js--CatalogMenu__category-items'):
        title = c.next.attrs.get('data-title', None)
        name_in_url = c.next.attrs.get('data-category-alias', None)
        if title is not None and name_in_url is not None:
            main_categories.append({'human_name': title,
                                    'url_name': name_in_url,
                                    'link': 'https://www.citilink.ru/catalog/{0}/'.format(name_in_url),
                                    'img_link': ''})
    return main_categories


def request_subcategory_page(main_category_name):
    url = 'https://www.citilink.ru/catalog/{0}/'.format(main_category_name)
    print(url)
    s = requests.Session()
    s = get_header(s)
    r = s.get(url)
    print(r.status_code)
    soup = BeautifulSoup(r.text, 'html.parser')
    return soup


def is_products_page(parsing_result):
    categories_cnt = len(parsing_result.find_all('div', class_='CatalogCategoryCardWrapper__content-flex'))

    if categories_cnt == 0:
        return True


    return False


def get_subcategories_names(parsing_result):
    data = parsing_result.find_all('div', class_='CatalogCategoryCardWrapper__content-flex')[0]
    result = []
    for card in data.contents:
        link = card.next.contents[1].attrs['href']
        name = card.next.contents[0].next.next.attrs['alt']
        img_link = card.next.contents[0].next.next.attrs['src']
        result.append({'human_name': name,
                       'url_name': link.split('/')[-2],
                       'link': link,
                       'img_link': img_link})
    return result


def create_subcategory_array(main_categories):

    categories_array = []
    cnt = 0
    for main_category in main_categories:
        time.sleep(5)
        try:
            parsing_result = request_subcategory_page(main_category['url_name'])
        except requests.exceptions.TooManyRedirects:
            print('request error')
            continue

        if not is_products_page(parsing_result):
            subcategories = get_subcategories_names(parsing_result)
            for subcategory in subcategories:

                try:
                    parsing_result = request_subcategory_page(subcategory['url_name'])
                    categories_array.append({'root': main_category['url_name'],
                                             'value': subcategory})
                    categories_array[-1]['value']['is_product_page'] = is_products_page(parsing_result)
                except:
                    print('request error')
                    continue

            print(subcategories)
        else:
            print(main_category['url_name'])
            value = main_category
            categories_array.append({'root': main_category['url_name'], 'value': value})
            categories_array[-1]['value']['is_product_page'] = True
            print(main_category['url_name'])
        cnt += 1
        print('{0}/{1}'.format(cnt, len(main_categories)))
    return categories_array


def get_all_categories_data(main_category):
    last_result = []

    result1 = create_subcategory_array(main_category)

    dop_cat = []
    for result in result1:
        last_result.append(result)
        if not result['value']['is_product_page']:
            dop_cat.append({'human_name': result['value']['human_name'],
                            'url_name': result['value']['url_name'],
                            'link': result['value']['link'],
                            'img_link': result['value']['img_link']})

    result2 = create_subcategory_array(dop_cat)
    #result2 = create_subcategory_array([{'url_name': 'telefoniya'}])
    for result in result2:
        if result['value']['is_product_page']:
            last_result.append(result)

    return last_result


def work_with_categories(main_category, file_name):
    last_result = get_all_categories_data(main_category)
    with open('categories_data_{0}.json'.format(file_name), 'wb') as fp:
        data = json.dumps(last_result, indent=4, ensure_ascii=False).encode('utf8')
        fp.write(data)


def get_products_info(category_name, max_products_cnt):
    all_products = []
    last_page = False
    page_number = 1
    while not last_page:
        req_cnt = 0
        products = []
        while len(products) == 0:
            products, page_soup = get_products_data_from_citilink(category_name, page_number)
            req_cnt += 1
            if req_cnt >= 5:
                return False, []
                break
            else:
                time.sleep(5)

        last_page = is_last_page(page_soup, page_number)
        all_products += products
        if len(all_products) >= max_products_cnt:
            all_products = all_products[0:max_products_cnt]
            break
        print(page_number)
        page_number += 1
        time.sleep(5)
    return True, all_products


def delete_extra_signs(val_str):
    i = 0
    for letter in val_str:
        if letter != '\n' and letter != ' ':
            break
        else:
            i += 1
    rez = val_str[i:-1]
    i = 0
    for letter in rez:
        if letter == '\n':
            break
        else:
            i += 1
    rez = rez[0:i]
    return rez


def get_specification_data(specification_val):
    rez = {}
    title_tag = specification_val.find_all('h4', class_='Heading Heading_level_4 SpecificationsFull__title')
    if len(title_tag) == 1:
        val = title_tag[0].next
        title = delete_extra_signs(val)
        for specification in specification_val.find_all('div', class_='Specifications__row'):
            name = specification.find_all('div', class_='Specifications__column Specifications__column_name')[0].next
            name = delete_extra_signs(name)
            val = specification.find_all('div', class_='Specifications__column Specifications__column_value')[0].next
            val = delete_extra_signs(val)
            rez[name] = val
        return True, title, rez
    return False, '', rez


def get_main_properties(page_soup):
    main_properties_tags = page_soup.find_all('p', class_='ProductPageMainPropertiesSection__property')
    rez = {}
    for main_property_tag in main_properties_tags:
        name = main_property_tag.contents[0].next
        name = delete_extra_signs(name)
        val = main_property_tag.contents[1].next
        val = delete_extra_signs(val)
        if val[-1] == ',':
            val = val[0:-1]
        rez[name[0:-2]] = val
    return rez


def get_images(page_soup):
    image_links = []
    images_tags = page_soup.find_all('img', class_='ProductPageStickyGallery-gallery__image-lower PreviewListSmall__image Image')
    for image_tag in images_tags:
        img_link = image_tag.attrs['src']
        image_links.append(img_link)
    return image_links


def get_detailed_product_info(product_link):
    url = product_link + 'properties'
    s = requests.Session()
    s = get_header(s)
    r = s.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    params = {}
    for c in soup.find_all('div', class_='SpecificationsFull'):
        is_finded, title, rez = get_specification_data(c)
        if is_finded:
            params[title] = rez

    img_links = get_images(soup)
    main_properties = get_main_properties(soup)
    params['imgs_links'] = img_links
    params['main_params'] = main_properties
    return params


def get_detailed_product_data(product_url):
    cnt = 0
    while True:
        cnt += 1
        print(product_url)
        detailed_info = get_detailed_product_info(product_url)
        if len(detailed_info) > 2:
            return True, detailed_info
        if cnt > 10:
            time.sleep(5)
            return False, detailed_info
        else:
            time.sleep(5)


#main_categories = get_main_categories_data()
#for main_category in main_categories[10:len(main_categories)]:
#    work_with_categories([main_category], main_category['url_name'])

def get_products_data(category_name):
    result = []
    is_success, desired_products = get_products_info(category_name, 10)
    if is_success:
        for desired_product in desired_products:
            link = 'http://www.citilink.ru' + desired_product['detail_link']
            is_successfull, detailed_data = get_detailed_product_data(link)
            if is_successfull:
                result.append({'short_data': desired_product,
                               'detailed_data': detailed_data,
                               'link': link})
            time.sleep(5)
    else:
        return False, []
    return True, result


def save_product_data(category_name, products_data, cur_dir):

    with open(os.path.join(cur_dir, '{0}_products.json'.format(category_name)), 'wb') as fp:
        data = json.dumps(products_data, indent=4, ensure_ascii=False).encode('utf8')
        fp.write(data)

    if not os.path.exists(os.path.join(cur_dir, 'products_imgs')):
        os.mkdir(os.path.join(cur_dir, 'products_imgs'))

    for product_data in products_data:
        cnt = 0
        product_name = product_data['link']
        vals = product_name.split(sep='/')
        product_name = vals[-2]
        for img_link in product_data['detailed_data']['imgs_links']:
            cnt += 1
            file_content = requests.get(img_link)
            print(img_link)

            open(os.path.join(cur_dir, 'products_imgs', '{0}_{1}.jpg'.format(product_name, cnt)), 'wb').write(file_content.content)
            if cnt < 7:
                time.sleep(1)
            else:
                break


def load_and_save_products_data():
    d = os.path.dirname(__file__)
    with open(os.path.join(d, 'shop_cite', 'fixtures', 'other_categories_data_db.json'), 'r', encoding='utf-8') as fp:
        categories = json.load(fp)

    cnt = 0
    if not os.path.exists(os.path.join(d, 'test_data', 'products')):
        os.mkdir(os.path.join(d, 'test_data', 'products'))

    for category in categories[4:-1]:
        if not category['fields']['has_subcategories']:
            category_name = category['fields']['short_image_name']
            print(category_name)
            cur_dir = os.path.join(d, 'test_data', 'products', '{0}'.format(category_name))
            if not os.path.exists(cur_dir):
                os.mkdir(cur_dir)
                print('LOAD DATA')
                while True:
                    is_success, products_data = get_products_data(category_name)
                    if is_success:
                        break
                    else:
                        print('ERROR LOAD')
                        time.sleep(10)
                save_product_data(category_name, products_data, cur_dir)
    print(cnt)


def load_main_images():
    d = os.path.dirname(__file__)
    dir_name = os.path.join(d, 'test_data', 'products')
    dir_list = os.listdir(dir_name)
    for folder in dir_list:
        if os.path.isdir(os.path.join(dir_name, folder)):
            file_name = os.path.join(dir_name, folder, folder + '_products.json')
            if os.path.exists(file_name):
                with open(file_name, 'r', encoding='utf-8') as fp:
                    products = json.load(fp)
                    for product in products:
                        img_link = product['short_data']['image_link']
                        file_content = requests.get(img_link)
                        product_name = product['short_data']['detail_link']
                        vals = product_name.split(sep='/')
                        product_name = vals[-2]

                        img_file_name = os.path.join(dir_name, folder, 'products_imgs', '{0}_{1}.jpg'.format(product_name, 'main'))
                        print('{0}_{1}.jpg'.format(product_name, 'main'))
                        open(img_file_name, 'wb').write(file_content.content)


def load_other_images():
    d = os.path.dirname(__file__)
    dir_name = os.path.join(d, 'test_data', 'products')
    dir_list = os.listdir(dir_name)
    for folder in dir_list:
        if os.path.isdir(os.path.join(dir_name, folder)):
            file_name = os.path.join(dir_name, folder, folder + '_products.json')
            if os.path.exists(file_name):
                with open(file_name, 'r', encoding='utf-8') as fp:
                    products = json.load(fp)
                    for product in products:
                        img_links = product['detailed_data']['imgs_links']
                        cnt = 0
                        for img_link in img_links:
                            cnt += 1
                            dimg_link = img_link[0:-6] + '_m.jpg'
                            print(img_link, dimg_link)
                            file_content = requests.get(dimg_link)
                            product_name = product['short_data']['detail_link']
                            vals = product_name.split(sep='/')
                            product_name = vals[-2]
                            img_file_name = os.path.join(dir_name, folder, 'products_imgs', '{0}_{1}_{2}.jpg'.format(product_name, 'm', cnt))
                            open(img_file_name, 'wb').write(file_content.content)
                            #print('{0}_{1}_{2}.jpg'.format(product_name, 'b', cnt))
                            if cnt > 2:
                                break

#load_main_images()
#load_and_save_products_data()

load_other_images()
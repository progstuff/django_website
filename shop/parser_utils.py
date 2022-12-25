import requests
from bs4 import BeautifulSoup
import time
import json
import random


def get_products_data_from_citilink(product_name, page_number):
    url = 'https://www.citilink.ru/catalog/{0}/?view_type=grid&p={1}'.format(product_name, page_number)
    r = requests.get(url)
    print(r)
    soup = BeautifulSoup(r.text, 'html.parser')
    products = []
    for c in soup.find_all('div', class_='ProductCardVerticalLayout ProductCardVertical__layout'):
        image_src = c.next.next.next.attrs['href']
        title = c.next.contents[2].next.next.attrs['title']
        product_link = c.next.contents[2].next.next.attrs['href']
        price = c.contents[1].next.next.next.contents[1].next.next.contents[0]
        price = price.replace(" ", "")
        price = price.replace("\n", "")
        products.append({'name': title,
                         'price': price,
                         'detail_link': product_link,
                         'image_link': image_src})

    return products


def get_main_categories_data():
    url = 'https://www.citilink.ru'
    r = requests.get(url)
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
    s.headers['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.131 Safari/537.36'
    r = s.get(url)
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
        time.sleep(random.randint(1, 3))
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


main_categories = get_main_categories_data()
for main_category in main_categories[10:len(main_categories)]:
    work_with_categories([main_category], main_category['url_name'])

#time.sleep(0.2)
#products = get_products_data_from_citilink(subcategories[5]['link'], 1)
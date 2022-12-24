import requests
from bs4 import BeautifulSoup
import time


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
                                    'url_name': name_in_url})
    return main_categories


def get_subcategory_name(main_category_name):
    url = 'https://www.citilink.ru/catalog/{0}/'.format(main_category_name)
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    data = soup.find_all('div', class_='CatalogCategoryCardWrapper__content-flex')[0]
    result = []
    for card in data.contents:
        link = card.next.contents[1].attrs['href']
        name = card.next.contents[0].next.next.attrs['alt']
        img_link = card.next.contents[0].next.next.attrs['src']
        result.append({'name': name,
                       'link': link,
                       'img_link': img_link})
    return result

main_categories = get_main_categories_data()
time.sleep(0.2)
subcategories = get_subcategory_name(main_categories[2]['url_name'])
time.sleep(0.2)
products = get_products_data_from_citilink(subcategories[5]['link'], 1)

a = 1
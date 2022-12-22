import requests
from bs4 import BeautifulSoup

url = 'https://www.citilink.ru/catalog/smartfony/?view_type=grid&p=2'
r = requests.get(url)
print(r)
soup = BeautifulSoup(r.text, 'html.parser')

for c in soup.find_all('div', class_='ProductCardVerticalLayout ProductCardVertical__layout'):
    a = c
    image_src = c.next.next.next.attrs['href']
    title = c.next.contents[2].next.next.attrs['title']
    product_link = c.next.contents[2].next.next.attrs['href']
    price = c.contents[1].next.next.next.contents[1].next.next.contents[0]
    price = price.replace(" ", "")
    price = price.replace("\n", "")
    print(image_src, title, product_link, price)


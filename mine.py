#!/usr/bin/python
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
from time import sleep

html = None
links = []
links_url = []

# pars page from products URLs
def get_listing(url):
    r = requests.get(url)
    htdoc = r.text

    try:
        if r.status_code == 200:
            soup = BeautifulSoup(htdoc, 'html.parser')
            for link in soup.find_all('li', class_='col-xs-6'):        
                link_item = link.find('a', class_="campaign-item")
                link_url = link_item.get('href')   
                links_url.insert(len(links_url),link_url)
    except Exception as ex:
        print(str(ex))
    finally:
        return links_url


# parse a single item to get information
def parse(url):
    info = []
    title_text = '-'
    price_text = '-'
    brand_name = '-'

    try:
        r = requests.get(url, timeout=10)
        sleep(2)

        if r.status_code == 200:
            print
            'Processing..' + url
            html = r.text
            soup = BeautifulSoup(html, 'html.parser')
            title = soup.title.string
            print(title)
            brand = soup.find('div', class_='product-brand-name')
            print(brand.text)        
            price = soup.find('span', class_='new-price')
            print(price.text)
            

            info.append(url)
            info.append(title)
            info.append(price.text)
            info.append(brand.text)
           
    except Exception as ex:
        print(str(ex))
    finally:
        if len(info) > 0:
            return ','.join(info)
        else:
            return None


for page in (1,4):
    cars_links = get_listing('https://www.fashiondays.ro/g/barbati-/imbracaminte-bluze?page='+ str(page))
    print(cars_links)

car_links = None
cars_info = []

for car in cars_links:
    cars_info.append(parse(car))
    if len(cars_info) > 0:
        with open('data.csv', 'a+') as f:
             f.write('\n'.join(cars_info))



# encoding: utf-8
import re
import string
import sys
import traceback

from motorcycle import RecordCreator
from common import make_soup, url_base


def process_todays_ads():
    ads_url = 'https://www.ss.lv/lv/transport/moto-transport/motorcycles/today/sell/'
    soup = make_soup(ads_url)

    results = soup.find_all('tr', id=re.compile(r'tr_\d{8}'))
    try:
        for result in results:
            image_url = result.find_all('td', class_='msga2')[1].a.img['src'].replace('.th2.jpg', '.800.jpg')
            description = result.find('td', class_='msg2').div.a.string
            url = result.find('td', class_='msg2').div.a['href']
            motorcycle_data = result.find_all('td', class_='pp6')
    
            price = motorcycle_data[4].string
            if motorcycle_data[4].string is None:
                price = motorcycle_data[4].b.string

            motorcycle_record = {
                'make': motorcycle_data[0].string.encode('utf-8'),
                'model': motorcycle_data[1].string.encode('utf-8'),
                'year': motorcycle_data[2].string.encode('utf-8'),
                'motor': motorcycle_data[3].string.encode('utf-8'),
                'price': price.translate(string.digits).encode('utf-8'),
                'image-url': image_url.encode('utf-8'),
                'description': description.encode('utf-8'),
                'url': url_base + url
            }

            RecordCreator.create_record_if_new(motorcycle_record)
            
    except (AttributeError, KeyError):
        traceback.print_exception(*sys.exc_info())
        pass

def process_todays_ads_album():
    ads_url = 'https://www.ss.lv/lv/transport/moto-transport/motorcycles/today/sell/photo/'
    soup = make_soup(ads_url)

    results = soup.find_all('td', class_='ads_album_td')
    try:
        for result in results:
            ad_container = result.find_all('div')[0]
            image_url = ad_container.a.img['src'].replace('.t.jpg', '.800.jpg')
            url = ad_container.a['href']
            make_and_model = ad_container.find('div', class_='d5').get_text()
            make_year = ad_container.find('div', class_='d11').find_all('td')[1].get_text()
            motor = ad_container.find('div', class_='d11').find_all('td')[3].get_text()
            location = ad_container.find_all('div', class_='d3f2 s12')[0].get_text()
            price = ad_container.find_all('div', {'class':['d7', 'd7p']})[0].get_text()

            motorcycle_record = {
                'make': make_and_model.encode('utf-8'),
                'year': make_year.encode('utf-8'),
                'motor': motor.encode('utf-8'),
                'price': price.translate(string.digits).encode('utf-8'),
                'image-url': image_url.encode('utf-8'),
                'description': location.encode('utf-8'),
                'url': url_base + url
            }

            RecordCreator.create_record_if_new(motorcycle_record)

    except (AttributeError, KeyError):
        traceback.print_exception(*sys.exc_info())
        pass
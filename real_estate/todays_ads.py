# encoding: utf-8
import re
import traceback
import sys
import string
from common import retrieve_database, make_soup, notify_via_telegram, url_base
from tinydb import Query

def process():
    todays_ads_url = 'https://www.ss.lv/lv/real-estate/homes-summer-residences/today/sell/'
    soup = make_soup(todays_ads_url)

    results = soup.find_all('tr', id=re.compile(r'tr_\d{8}'))
    try:
        for result in results:        
            image_url = result.find_all('td', class_='msga2')[1].a.img['src']
            description = result.find('td', class_='msg2').div.a.string
            url = result.find('td', class_='msg2').div.a['href']
            main_data = result.find_all('td', class_='pp6')
            create_record_if_new(main_data, image_url, description, url)

    except (AttributeError, KeyError):
        traceback.print_exception(*sys.exc_info())
        pass

def create_record_if_new(main_data, motorcycle_image, description, url):
    db = retrieve_database()
    table = db.table('advertisments')
    
    price = main_data[5].string
    if main_data[5].string is None:
        price = main_data[5].b.string

    rec = {
        'location': main_data[0].string.encode('utf-8'),
        'area': main_data[1].string.encode('utf-8'),
        'stories': main_data[2].string.encode('utf-8'),
        'rooms': main_data[3].string.encode('utf-8'),
        'land_area': main_data[4].string.encode('utf-8'),
        'price': price.translate(string.digits).encode('utf-8'),
        'image-url': motorcycle_image.encode('utf-8'),
        'description': description.encode('utf-8'),
        'url': url_base + url
    }
    Result = Query()
    entry_exists = table.search(Result.location == rec['location'] and Result.area == rec['area'] and Result.rooms == rec['rooms'] and Result.price == rec['price'])
    if not entry_exists:
        message = ('Māja: {} {} kvm\n{}. stāvi, {}. istabas\nZeme: {}\nCena: {}\nSkatīt: {}').format(rec['location'], rec['area'], rec['stories'], rec['rooms'], rec['land_area'], rec['price'], rec['url'])
        notify_via_telegram(rec['image-url'], message)
        table.insert(rec)        
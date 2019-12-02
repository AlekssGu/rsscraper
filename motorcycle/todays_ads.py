# encoding: utf-8
import re
import traceback
import sys
import string
from common import retrieve_database, make_soup, notify_via_telegram, url_base
from tinydb import Query

def process():
    todays_ads_url = 'https://www.ss.lv/lv/transport/moto-transport/motorcycles/today/sell/'
    soup = make_soup(todays_ads_url)

    results = soup.find_all('tr', id=re.compile(r'tr_\d{8}'))
    try:
        for result in results:        
            image_url = result.find_all('td', class_='msga2')[1].a.img['src']
            description = result.find('td', class_='msg2').div.a.string
            url = result.find('td', class_='msg2').div.a['href']
            motorcycle_data = result.find_all('td', class_='pp6')
            create_record_if_new(motorcycle_data, image_url, description, url)

    except (AttributeError, KeyError):
        traceback.print_exception(*sys.exc_info())
        pass

def create_record_if_new(motorcycle_data, motorcycle_image, description, url):
    db = retrieve_database()
    table = db.table('motorcycles')
    
    price = motorcycle_data[4].string
    if motorcycle_data[4].string is None:
        price = motorcycle_data[4].b.string

    rec = {
        'make': motorcycle_data[0].string.encode('utf-8'),
        'model': motorcycle_data[1].string.encode('utf-8'),
        'year': motorcycle_data[2].string.encode('utf-8'),
        'motor': motorcycle_data[3].string.encode('utf-8'),
        'price': price.translate(string.digits).encode('utf-8'),
        'image-url': motorcycle_image.encode('utf-8'),
        'description': description.encode('utf-8'),
        'url': url_base + url
    }
    Result = Query()
    entry_exists = table.search(Result.make == rec['make'] and Result.model == rec['model'] and Result.year == rec['year'] and Result.price == rec['price'])
    if not entry_exists:
        message = ('Motocikls: {} {}\nGads: {}\nCena: {}\nSkatīt: {}').format(rec['make'], rec['model'], rec['year'], rec['price'], rec['url'])
        notify_via_telegram(rec['image-url'], message)
        table.insert(rec)        
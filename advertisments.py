# encoding: utf-8
import re
import traceback
import sys
from common import retrieve_database, make_soup
from tinydb import Query

def process():
    db = retrieve_database()

    for category in db.table('motorcycle_categories'):
        soup = make_soup(category['category-url'])
        table_name = category['category'].encode('utf-8').lower().replace('- ', '_')
        table_name = table_name.replace('čžņēš', 'x')
        table = db.table(table_name)
            
        results = soup.find_all('tr', id=re.compile('tr_\d{8}'))
        try:
            for result in results:        
                motorcycle_image = result.find_all('td', class_='msga2')[1].a.img['src']
                motorcycle_data = result.find_all('td', class_='pp6')
                rec = {
                    'model': motorcycle_data[0].string,
                    'year': motorcycle_data[1].string,
                    'motor': motorcycle_data[2].string,
                    'price': motorcycle_data[3].string,
                    'image-url': motorcycle_image
                }
                Result = Query()
                entry_exists = table.search(Result.model == motorcycle_data[0].string and Result.year == motorcycle_data[1].string)
                if not entry_exists:
                    table.insert(rec)

        except (AttributeError, KeyError):
            traceback.print_exception(*sys.exc_info())
            pass
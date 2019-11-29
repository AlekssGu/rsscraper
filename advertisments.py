# encoding: utf-8
import re
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
                print result
                #motorcycle = result.td
                # rec = {
                #     'category': category,
                #     'category-url': url_base + result.a['href']
                # }

                # Result = Query()
                # entry_exists = table.search(Result.category == category)

                # if not entry_exists:
                #     table.insert(rec)
        except (AttributeError, KeyError) as ex:
            print ex
            pass
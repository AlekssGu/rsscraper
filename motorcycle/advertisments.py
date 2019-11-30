# encoding: utf-8
import re
import traceback
import sys
from common import retrieve_database, make_soup
from tinydb import Query

def process():
    db = retrieve_database()

    for motorycle_make in db.table('motorcycle_categories'):
        soup = make_soup(motorycle_make['category-url'])
        table = db.table('motorcycles')
        results = soup.find_all('tr', id=re.compile(r'tr_\d{8}'))
        try:
            for result in results:        
                motorcycle_image = result.find_all('td', class_='msga2')[1].a.img['src']
                motorcycle_data = result.find_all('td', class_='pp6')
                if len(motorcycle_data) >= 4:
                    create_record_if_new(table, motorycle_make['category'], motorcycle_data, motorcycle_image)

        except (AttributeError, KeyError):
            traceback.print_exception(*sys.exc_info())
            pass

def normalized_table_name(table_name):
    table_name = table_name.encode('utf-8').lower().replace('- ', '_')
    table_name = table_name.replace('čžņēš', 'x')
    return table_name

def create_record_if_new(table, make, motorcycle_data, motorcycle_image):
    rec = {
        'make': make,
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

def fill_xls(db, workbook):
    worksheet = workbook.add_worksheet()
    worksheet.name = 'Motorcycles'
    worksheet.set_column(0,0, 20)
    worksheet.set_column(1,1, 20)  
    worksheet.set_column(2,2, 20)  
    worksheet.set_column(3,3, 20) 
    worksheet.set_column(4,4, 20) 
    worksheet.set_column(5,5, 20) 

    Headlines = ["Make", "Model", "Year", "Motor capacity", "Price", "Image URL"]
    row = 0 
    for col, title in enumerate(Headlines):
        worksheet.write(row, col, title)

    for item in db.table('motorcycles'):
        row += 1
        worksheet.write(row, 0, item['make'])
        worksheet.write(row, 1, item['model'])       
        worksheet.write(row, 2, item['year'])       
        worksheet.write(row, 3, item['motor'])       
        worksheet.write(row, 4, item['price'])        
        worksheet.write(row, 5, item['image-url'])        
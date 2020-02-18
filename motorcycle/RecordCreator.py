# encoding: utf-8
from common import retrieve_database, notify_via_telegram
from tinydb import Query


def create_record_if_new(motorcycle_data):
    db = retrieve_database()
    table = db.table('motorcycles')

    Result = Query()
    entry_exists = table.search(
        Result.make == motorcycle_data['make'] and Result.model == motorcycle_data['model'] and Result.year ==
        motorcycle_data['year'] and Result.price == motorcycle_data['price'])
    if not entry_exists:
        table.insert(motorcycle_data)
        notify(motorcycle_data)


def notify(motorcycle_data):
    message = ('Motocikls: {} {}\nGads: {}\nCena: {}\nSkatīt: {}').format(motorcycle_data['make'],
                                                                          motorcycle_data['model'],
                                                                          motorcycle_data['year'],
                                                                          motorcycle_data['price'],
                                                                          motorcycle_data['url'])
    notify_via_telegram(motorcycle_data['image-url'], message)


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
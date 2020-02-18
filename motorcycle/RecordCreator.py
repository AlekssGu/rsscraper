# encoding: utf-8
from tinydb import Query

from common import retrieve_database, notify_via_telegram


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
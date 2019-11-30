from common import url_base, retrieve_database, make_soup
from tinydb import Query  

def process():
    url = url_base + '/transport/moto-transport/motorcycles'
    soup = make_soup(url)
    db = retrieve_database()
    table = db.table('motorcycle_categories')

    results = soup.find_all("h4", class_="category")
    try:
        for result in results:        
            category = result.a.string.strip().encode('utf-8')
            rec = {
                'category': category,
                'category-url': url_base + result.a['href']
            }

            Result = Query()
            entry_exists = table.search(Result.category == category)

            if not entry_exists:
                table.insert(rec)
    except (AttributeError, KeyError):
        pass

def fill_xls(db, workbook):
    worksheet = workbook.add_worksheet()
    worksheet.name = 'Motorcycle categories'
    worksheet.set_column(0,0, 15) # category
    worksheet.set_column(1,1, 20) # category URL

    Headlines = ["Category", "Category URL"]
    row = 0 
    for col, title in enumerate(Headlines):
        worksheet.write(row, col, title)

    for item in db.table('motorcycle_categories'):
        row += 1
        worksheet.write(row, 0, item['category'])
        worksheet.write(row, 1, item['category-url'])
import xlsxwriter
from common import retrieve_database
import categories

def make_excel():
    db = retrieve_database()
    workbook = xlsxwriter.Workbook('motorcycles.xlsx')
    worksheet = workbook.add_worksheet()

    categories.fill_xls(db, worksheet)

    workbook.close()
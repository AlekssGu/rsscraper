import xlsxwriter
from common import retrieve_database
import motorcycle

def make_excel():
    db = retrieve_database()
    workbook = xlsxwriter.Workbook('data_export.xlsx')
    worksheet = workbook.add_worksheet()

    motorcycle.categories.fill_xls(db, worksheet)

    workbook.close()
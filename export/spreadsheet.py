import xlsxwriter
from common import retrieve_database
import motorcycle

def make_excel():
    db = retrieve_database()
    workbook = xlsxwriter.Workbook('data_export.xlsx')
    
    motorcycle.categories.fill_xls(db, workbook)
    motorcycle.advertisments.fill_xls(db, workbook)

    workbook.close()
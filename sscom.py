import common
import categories
import advertisments
import spreadsheet

def main():
    soup_process()
    spreadsheet.make_excel()

def soup_process():  
    categories.process()
    advertisments.process()

main()
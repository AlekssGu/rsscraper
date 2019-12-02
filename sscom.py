import time
import common
from motorcycle import Motorcycle
from real_estate import RealEstate
from export import spreadsheet

def main():
    soup_process()
    spreadsheet.make_excel()

def process_todays_ads():
    RealEstate.process_todays_ads()
    Motorcycle.process_todays_ads()

def soup_process():  
    Motorcycle.process()

while True:
    process_todays_ads()
    time.sleep(300)
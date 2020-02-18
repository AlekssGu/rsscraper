import time

from motorcycle import Motorcycle
from real_estate import RealEstate
from system_parameters import DEFAULT_SLEEP_TIME_IN_SECONDS


def main():
    #RealEstate.process_ads_of_this_day()
    Motorcycle.process_ads_of_this_day()


while True:
    main()
    time.sleep(DEFAULT_SLEEP_TIME_IN_SECONDS)

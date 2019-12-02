import urllib3
import system_parameters
import telegram
from tinydb import TinyDB
from bs4 import BeautifulSoup

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
url_base = 'https://www.ss.lv'

def retrieve_database():
    return TinyDB("db.json")

def make_soup(url):
    http = urllib3.PoolManager()
    r = http.request("GET", url)
    return BeautifulSoup(r.data, 'lxml')

def notify_via_telegram(photo, message):
    my_token = system_parameters.TELEGRAM_TOKEN
    chat_id = system_parameters.TELEGRAM_CHAT_ID
    bot = telegram.Bot(token=my_token)
    bot.send_photo(chat_id=chat_id, photo=photo, caption=message)
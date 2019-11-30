import common
import categories
import advertisments
import spreadsheet
import telegram
import system_parameters

def main():
    soup_process()
    spreadsheet.make_excel()

def soup_process():  
    categories.process()
    advertisments.process()

def notify_via_telegram():
    my_token = system_parameters.TELEGRAM_TOKEN
    chat_id = system_parameters.TELEGRAM_CHAT_ID
    bot = telegram.Bot(token=my_token)
    bot.sendMessage(chat_id=chat_id, text='Update')

main()
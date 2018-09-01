import logging
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
from get_events import get_events

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

TOKEN = 'YOUR_TOKEN'
REQUEST_KWARGS = {
    #'proxy_url': 'http://213.239.209.51:3128',
    # Optional, if you need authentication:
    # 'urllib3_proxy_kwargs': {
    #     'username': 'PROXY_USER',
    #     'password': 'PROXY_PASS',
    # }
}


def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="I'm a super bot, i know /calendar command!")


def echo(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="use commands with slash(/) please")


def unknown(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="sorry, I understand only /calendar command.")


def calendar(bot, update):
    events = get_events()
    res = ""
    for ev in events:
        res += str(ev[0]) + ' ' + str(ev[1]) + '\n'
    if len(events)==0:
        res = "no events found for next 24h"
    bot.send_message(chat_id=update.message.chat_id, text=res)


def run_bot():
    updater = Updater(TOKEN, request_kwargs=REQUEST_KWARGS)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start))

    dispatcher.add_handler(MessageHandler(Filters.text, echo))

    dispatcher.add_handler(CommandHandler('calendar', calendar))

    dispatcher.add_handler(MessageHandler(Filters.command, unknown))

    updater.start_polling()
    updater.idle()
    print("telegram bot done")


if __name__ == "__main__":
    run_bot()

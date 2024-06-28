from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

from handlers import setup_dispatcher
from settings import TELEGRAM_TOKEN, HEROKU_APP_NAME, PORT

def main():
    print(f"Running bot in webhook mode. Make sure that this url is correct: https://{HEROKU_APP_NAME}.herokuapp.com/")

    updater = Updater(token=TELEGRAM_TOKEN, use_context=True)

    setup_dispatcher(updater)

    updater.start_webhook(
        listen="0.0.0.0",
        port=PORT,
        url_path=TELEGRAM_TOKEN
    )
    updater.bot.set_webhook(f"https://{HEROKU_APP_NAME}.herokuapp.com/{TELEGRAM_TOKEN}".format(HEROKU_APP_NAME, TOKEN))

if __name__ == "__main__":
    main()

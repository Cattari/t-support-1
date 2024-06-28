from telegram.ext import Updater, Application
from telegram import Update

from handlers import setup_dispatcher
from settings import TELEGRAM_TOKEN, HEROKU_APP_NAME, PORT

def main():
    print(f"Running bot in webhook mode. Make sure that this url is correct: https://{HEROKU_APP_NAME}.herokuapp.com/")

    application = (
        Application.builder()
        .token(TELEGRAM_TOKEN)
        .build()
    )

    setup_dispatcher(application)

    application.run_webhook(
        listen="0.0.0.0",                          
        port=int(PORT),                          
        webhook_url=f"https://{HEROKU_APP_NAME}.herokuapp.com/{TELEGRAM_TOKEN}"
    )


if __name__ == "__main__":
    main()

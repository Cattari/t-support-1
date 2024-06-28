from telegram.ext import (
    Application, 
    ContextTypes, 
    CallbackContext,
    TypeHandler,
    ExtBot
)
from telegram import Update

import asyncio
from http import HTTPStatus
from dataclasses import dataclass
from handlers import setup_dispatcher
from settings import TELEGRAM_TOKEN, HEROKU_APP_NAME, PORT

import uvicorn
from asgiref.wsgi import WsgiToAsgi
from flask import Flask, Response, abort, make_response, request

@dataclass
class WebhookUpdate:
    """Simple dataclass to wrap a custom update type"""

    user_id: int
    payload: str
class CustomContext(CallbackContext[ExtBot, dict, dict, dict]):
    """
    Custom CallbackContext class that makes `user_data` available for updates of type
    `WebhookUpdate`.
    """

    @classmethod
    def from_update(
        cls,
        update: object,
        application: "Application",
    ) -> "CustomContext":
        if isinstance(update, WebhookUpdate):
            return cls(application=application, user_id=update.user_id)
        return super().from_update(update, application)

async def main():
    print(f"Running bot in webhook mode. Make sure that this url is correct: https://{HEROKU_APP_NAME}.herokuapp.com/")

    context_types = ContextTypes(context=CustomContext)
    application = (
        Application.builder().token(TELEGRAM_TOKEN).updater(None).context_types(context_types).build()
    )

    # Pass webhook settings to telegram
    await application.bot.set_webhook(url=f"https://{HEROKU_APP_NAME}.herokuapp.com/telegram", allowed_updates=Update.ALL_TYPES)

    # Set up webserver
    flask_app = Flask(__name__)

    @flask_app.post("/telegram")  # type: ignore[misc]
    async def telegram() -> Response:
        """Handle incoming Telegram updates by putting them into the `update_queue`"""
        await application.update_queue.put(Update.de_json(data=request.json, bot=application.bot))
        return Response(status=HTTPStatus.OK)
    
    @flask_app.get("/healthcheck")  # type: ignore[misc]
    async def health() -> Response:
        """For the health endpoint, reply with a simple plain text message."""
        response = make_response("The bot is still running fine :)", HTTPStatus.OK)
        response.mimetype = "text/plain"
        return response
    
    setup_dispatcher(application)

    webserver = uvicorn.Server(
        config=uvicorn.Config(
            app=WsgiToAsgi(flask_app),
            port=PORT,
            use_colors=False,
            host=f"https://{HEROKU_APP_NAME}.herokuapp.com/",
        )
    )

    # Run application and webserver together
    async with application:
        await application.start()
        await webserver.serve()
        await application.stop()

if __name__ == "__main__":
    asyncio.run(main())


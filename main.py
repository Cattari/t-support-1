from telegram.ext import Application
from telegram import Update

import uvicorn
from http import HTTPStatus
from contextlib import asynccontextmanager
from handlers import setup_dispatcher
from settings import TELEGRAM_TOKEN, HEROKU_APP_NAME, PORT

from fastapi import FastAPI, Request, Response

print(f"Running bot in webhook mode. Make sure that this url is correct: https://{HEROKU_APP_NAME}.herokuapp.com/")

ptb = (
    Application.builder()
        .updater(None)
        .token(TELEGRAM_TOKEN) # replace <your-bot-token>
        .read_timeout(7)
        .get_updates_read_timeout(42)
        .build()
)

@asynccontextmanager
async def lifespan(_: FastAPI):
    await ptb.bot.setWebhook(f"https://{HEROKU_APP_NAME}.herokuapp.com/{TELEGRAM_TOKEN}") # replace <your-webhook-url>
    setup_dispatcher(ptb)
    ptb.run_webhook()
    async with ptb:
        await ptb.start()
        yield
        await ptb.stop()

# Initialize FastAPI app (similar to Flask)
app = FastAPI(lifespan=lifespan)

@app.post("/telegram")
async def process_update(request: Request):
    req = await request.json()
    update = Update.de_json(req, ptb.bot)
    await ptb.process_update(update)
    return Response(status_code=HTTPStatus.OK)

@app.get("/hc")  # type: ignore[misc]
async def health(request: Request) -> Response:
    """For the health endpoint, reply with a simple plain text message."""
    return Response(status_code=HTTPStatus.OK, content="OK")



if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=PORT)


from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from telegram import Update
from settings import (
    BAN_MESSAGE,
    PRIVATE_KEY_DANGEROUS_COMMAND, 
    WELCOME_MESSAGE, 
    TELEGRAM_SUPPORT_CHAT_ID,
)
from cachetools import TTLCache

bot_forward_data = TTLCache(maxsize=1000, ttl=60*60*24*2)
"""message_id - user_id; cache time for each key/message - 2 days"""

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(WELCOME_MESSAGE)

    user_info = update.message.from_user.to_dict()

    context.bot.send_message(
        chat_id=TELEGRAM_SUPPORT_CHAT_ID,
        text=f"""
📞 Connected {user_info}.
        """,
    )

async def ban(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(BAN_MESSAGE)

    user_id = None

    if bot_forward_data[update.message.reply_to_message.id]:
        user_id = bot_forward_data[update.message.reply_to_message.id]

    await context.bot.send_message(
        chat_id=user_id,
        text="You are banned forever",
    )

async def clear_forward_data(update: Update, context: ContextTypes.DEFAULT_TYPE):
    bot_forward_data.clear()
    await update.message.reply_text('Cleared forward data')

async def forward_to_chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    forwardedMessage = await update.message.forward(chat_id=TELEGRAM_SUPPORT_CHAT_ID, api_kwargs={'user_id': user_id})
    bot_forward_data[forwardedMessage.id] = user_id 

async def forward_to_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = None

    if bot_forward_data[update.message.reply_to_message.id]:
        user_id = bot_forward_data[update.message.reply_to_message.id]
    is_reply_to_forwarded_by_bot = update.message.reply_to_message.from_user.is_bot
    if user_id and is_reply_to_forwarded_by_bot:
        await context.bot.copy_message(
            message_id=update.message.message_id,
            chat_id=user_id,
            from_chat_id=update.message.chat_id
        )


def setup_dispatcher(application: Application):
    application.add_handler(CommandHandler('start', start))
    if PRIVATE_KEY_DANGEROUS_COMMAND:
        application.add_handler(
            CommandHandler(
                f"clear-reply-data-${PRIVATE_KEY_DANGEROUS_COMMAND}", 
                clear_forward_data
            )
        )
    application.add_handler(MessageHandler(filters.ChatType.PRIVATE, forward_to_chat))
    application.add_handler(
        CommandHandler('ban', ban, filters.Chat(TELEGRAM_SUPPORT_CHAT_ID) & filters.REPLY)
    )
    application.add_handler(MessageHandler(filters.Chat(TELEGRAM_SUPPORT_CHAT_ID) & filters.REPLY, forward_to_user))


    return application

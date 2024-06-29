from telegram.ext import CommandHandler, MessageHandler, filters, ContextTypes
from telegram import Update
from settings import BAN_MESSAGE, WELCOME_MESSAGE, TELEGRAM_SUPPORT_CHAT_ID, REPLY_TO_THIS_MESSAGE, WRONG_REPLY

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

    user_info = update.message.from_user.to_dict()

    update

    await context.bot.send_message(
        chat_id=TELEGRAM_SUPPORT_CHAT_ID,
        text=f"""
Banned {user_info}.
        """,
    )

async def mute(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(BAN_MESSAGE)

    user_info = update.message.from_user.to_dict()

    update

    await context.bot.send_message(
        chat_id=TELEGRAM_SUPPORT_CHAT_ID,
        text=f"""
Banned {user_info}.
        """,
    )


async def forward_to_chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """{ 
        'message_id': 5, 
        'date': 1605106546, 
        'chat': {'id': 49820636, 'type': 'private', 'username': 'danokhlopkov', 'first_name': 'Daniil', 'last_name': 'Okhlopkov'}, 
        'text': 'TEST QOO', 'entities': [], 'caption_entities': [], 'photo': [], 'new_chat_members': [], 'new_chat_photo': [], 'delete_chat_photo': False, 'group_chat_created': False, 'supergroup_chat_created': False, 'channel_chat_created': False, 
        'from': {'id': 49820636, 'first_name': 'Daniil', 'is_bot': False, 'last_name': 'Okhlopkov', 'username': 'danokhlopkov', 'language_code': 'en'}
    }"""
    forwarded = await update.message.forward(chat_id=TELEGRAM_SUPPORT_CHAT_ID)
    # await context.bot.send_message(
    #     chat_id=TELEGRAM_SUPPORT_CHAT_ID,
    #     reply_to_message_id=forwarded.message_id,
    #     text=f'{update.message.from_user.id}\n{REPLY_TO_THIS_MESSAGE}'
    # )


async def forward_to_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """{
        'message_id': 10, 'date': 1605106662, 
        'chat': {'id': -484179205, 'type': 'group', 'title': '☎️ SUPPORT CHAT', 'all_members_are_administrators': True}, 
        'reply_to_message': {
            'message_id': 9, 'date': 1605106659, 
            'chat': {'id': -484179205, 'type': 'group', 'title': '☎️ SUPPORT CHAT', 'all_members_are_administrators': True}, 
            'forward_from': {'id': 49820636, 'first_name': 'Daniil', 'is_bot': False, 'last_name': 'Okhlopkov', 'danokhlopkov': 'okhlopkov', 'language_code': 'en'}, 
            'forward_date': 1605106658, 
            'text': 'g', 'entities': [], 'caption_entities': [], 'photo': [], 'new_chat_members': [], 'new_chat_photo': [], 
            'delete_chat_photo': False, 'group_chat_created': False, 'supergroup_chat_created': False, 'channel_chat_created': False, 
            'from': {'id': 1440913096, 'first_name': 'SUPPORT', 'is_bot': True, 'username': 'lolkek'}
        }, 
        'text': 'ggg', 'entities': [], 'caption_entities': [], 'photo': [], 'new_chat_members': [], 'new_chat_photo': [], 'delete_chat_photo': False, 
        'group_chat_created': False, 'supergroup_chat_created': False, 'channel_chat_created': False, 
        'from': {'id': 49820636, 'first_name': 'Daniil', 'is_bot': False, 'last_name': 'Okhlopkov', 'username': 'danokhlopkov', 'language_code': 'en'}
    }"""
    user_id = None
    print('FROM USER')
    print(update.message.from_user)

    if update.message.from_user:
        user_id = update.message.from_user.id
    # is_user_in_chat = bool(await update.message.chat.get_member(user_id))
    is_reply_to_bot = update.message.from_user.is_bot

    if user_id and is_reply_to_bot:
        await context.bot.copy_message(
            message_id=update.message.message_id,
            chat_id=user_id,
            from_chat_id=update.message.chat_id
        )
    else:
        await context.bot.send_message(
            chat_id=TELEGRAM_SUPPORT_CHAT_ID,
            text=WRONG_REPLY
        )


def setup_dispatcher(application):
    application.add_handler(CommandHandler('start', start))
    application.add_handler(MessageHandler(filters.ChatType.PRIVATE, forward_to_chat))
    application.add_handler(MessageHandler(filters.Chat(TELEGRAM_SUPPORT_CHAT_ID) & filters.REPLY, forward_to_user))
    return application

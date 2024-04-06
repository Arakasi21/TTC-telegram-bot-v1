from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, CallbackContext, CallbackQueryHandler
from telegram.ext.filters import _Photo
from commands.start import start
from commands.register import register
from commands.submit_request import submit_request
from commands.get_requests import get_requests
from commands.handle_photo import handle_photo
from commands.take_request import take_request
from commands.close_request import close_request
from settings.config import TOKEN
import logging

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(message)s', level=logging.INFO
)

logging.getLogger("httpx").setLevel(logging.WARNING)

logging.getLogger("httpx").setLevel(logging.INFO)

logger = logging.getLogger(__name__)

chat_sessions = {}

async def callback_query_handler(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()
    
    action, user_id = query.data.split("_")
    
    if action == "chat":
        chat_sessions[query.message.chat_id] = {"client_id": user_id}
        await context.bot.send_message(chat_id=query.message.chat_id, text="Чат с пользователем начат.")

async def message_handler(update: Update, context: CallbackContext):
    from_id = update.effective_chat.id
    text = update.message.text

    # ОТ админа К клиенту
    if from_id in chat_sessions:
        client_id = chat_sessions[from_id]["client_id"]
        await context.bot.send_message(chat_id=client_id, text=text)
        return
    
    # ОТ клиента К админу
    for admin_id, session_info in chat_sessions.items():
        if session_info["client_id"] == str(from_id):
            await context.bot.send_message(chat_id=admin_id, text=text)
            return

async def close_chat(update: Update, context: CallbackContext):
    from_id = update.effective_chat.id
    if from_id in chat_sessions:
        del chat_sessions[from_id]
        await context.bot.send_message(chat_id=from_id, text="Чат завершен.")

def unknown_command(update: Update, context: CallbackContext):
    update.message.reply_text("Sorry, I couldn't recognize that command.")

def main() -> None:
    application = ApplicationBuilder().token(TOKEN).build()

    start_handler = CommandHandler('start', start)

    # переписать блок
    register_handler = CommandHandler('register', register)
    submit_request_handler = CommandHandler('submit_request', submit_request)
    get_requests_handler = CommandHandler('get_requests', get_requests)
    take_request_handler = CommandHandler('take_request', take_request)
    close_request_handler = CommandHandler('close_request', close_request)

    photo_handler = MessageHandler(filters.PHOTO, handle_photo)
    
    application.add_handler(photo_handler)
    application.add_handler(start_handler)
    application.add_handler(register_handler)

    application.add_handler(CallbackQueryHandler(callback_query_handler))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), message_handler))
    application.add_handler(CommandHandler("close", close_chat))

    application.add_handler(get_requests_handler)
    application.add_handler(take_request_handler)
    application.add_handler(close_request_handler)

    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), message_handler))

    application.run_polling()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())

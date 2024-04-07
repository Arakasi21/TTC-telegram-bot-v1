from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, CallbackContext, CallbackQueryHandler, ConversationHandler
from telegram.ext.filters import _Photo
from commands.start import start
from commands.register import register
from commands.get_requests import get_requests
from commands.handle_photo import handle_photo
from commands.take_request import take_request
from commands.close_request import close_request
from commands.chat import callback_query_handler, message_handler, close_chat
from settings.config import TOKEN
import logging

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(message)s', level=logging.INFO
)

logging.getLogger("httpx").setLevel(logging.WARNING)

logging.getLogger("httpx").setLevel(logging.INFO)

logger = logging.getLogger(__name__)

def unknown_command(update: Update, context: CallbackContext):
    update.message.reply_text("Sorry, I couldn't recognize that command.")


async def cancel(update: Update, context: CallbackContext) -> int:
    return ConversationHandler.END

def main() -> None:
    application = ApplicationBuilder().token(TOKEN).build()

    start_handler = CommandHandler('start', start)

    # переписать блок
    register_handler = CommandHandler('register', register)

    # admin functionality
    get_requests_handler = CommandHandler('get_requests', get_requests)
    take_request_handler = CommandHandler('take_request', take_request)
    close_request_handler = CommandHandler('close_request', close_request)

    # user sending photo and creating request
    photo_handler = MessageHandler(filters.PHOTO, handle_photo)
    
    application.add_handler(start_handler)
    application.add_handler(photo_handler)
    application.add_handler(register_handler)

    # chat
    application.add_handler(CallbackQueryHandler(callback_query_handler))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), message_handler))
    application.add_handler(CommandHandler("close", close_chat))

    # admin function's handler
    application.add_handler(get_requests_handler)
    application.add_handler(take_request_handler)
    application.add_handler(close_request_handler)

    application.run_polling()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())

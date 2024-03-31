from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters

from commands.start import start
from commands.register import register
from commands.submit_request import submit_request
from commands.get_requests import get_requests
from commands.handle_photo import handle_photo

from settings.config import TOKEN
import logging

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(message)s', level=logging.INFO
)

logging.getLogger("httpx").setLevel(logging.WARNING)

logging.getLogger("httpx").setLevel(logging.INFO)

logger = logging.getLogger(__name__)

def unknown_command(update, context):
    update.message.reply_text("Sorry, I couldn't recognize that command.")

def main() -> None:
    application = ApplicationBuilder().token(TOKEN).build()

    start_handler = CommandHandler('start', start)
    register_handler = CommandHandler('register', register)
    submit_request_handler = CommandHandler('submit_request', submit_request)
    get_requests_handler = CommandHandler('get_requests', get_requests)
    photo_handler = MessageHandler(Filters.photo, handle_photo)

    application.add_handler(start_handler)
    application.add_handler(register_handler)
    application.add_handler(submit_request_handler)
    application.add_handler(get_requests_handler)
    application.add_handler(MessageHandler(Filters.command, unknown_command))
    application.add_handler(photo_handler)
    

    application.run_polling()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())

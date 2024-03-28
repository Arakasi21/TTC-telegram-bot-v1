from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
from commands.start import start
from commands.register import register
from commands.submit_request import submit_request
from commands.get_requests import get_requests
from settings.config import TOKEN
import logging

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(message)s', level=logging.INFO
)

logging.getLogger("httpx").setLevel(logging.WARNING)

logging.getLogger("httpx").setLevel(logging.INFO)

logger = logging.getLogger(__name__)

def main() -> None:
    application = ApplicationBuilder().token(TOKEN).build()

    start_handler = CommandHandler('start', start)
    register_handler = CommandHandler('register', register)
    submit_request_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), submit_request)
    get_requests_handler = CommandHandler('get_requests', get_requests)

    application.add_handler(start_handler)
    application.add_handler(register_handler)
    application.add_handler(submit_request_handler)
    application.add_handler(get_requests_handler)

    application.run_polling()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())

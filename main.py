from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
from commands.start import start
from commands.submit_request import submit_request
from settings.config import TOKEN
import logging

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

def main() -> None:
    application = ApplicationBuilder().token(TOKEN).build()

    start_handler = CommandHandler('start', start)
    submit_request_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), submit_request)

    application.add_handler(start_handler)
    application.add_handler(submit_request_handler)


if __name__ == "__main__":
    main()

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters, CallbackContext, CallbackQueryHandler, ConversationHandler
from commands.start import start
from commands.register import register
from settings.constants import TAKE_REQ, CLOSE_REQ, CLOSE_CHAT, SUMBIT_PHOTO, SUBMIT_TEXT, SEND_FEEDBACK
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
logger = logging.getLogger(__name__)

def error_handler(update, context):
    """Log Errors caused by Updates."""
    logger.error(f'Update {update} caused error {context.error}')

def unknown_command(update: Update, context: CallbackContext):
    update.message.reply_text("Sorry, I couldn't recognize that command.")

async def cancel(update: Update, context: CallbackContext) -> int:
    update.message.reply_text("Вы завершили request cycle")
    return ConversationHandler.END

def main() -> None:
    application = ApplicationBuilder().token(TOKEN).build()
    start_handler = CommandHandler('start', start)
    register_handler = CommandHandler('register', register)

    # admin functionality
    admin_conv_handler = ConversationHandler(
        entry_points=[CommandHandler("get_requests",get_requests)],
        states={                                                                                                                                                       
            TAKE_REQ: [CommandHandler('take_request', take_request)],
            CLOSE_CHAT: [CommandHandler("close", close_chat)],
            CLOSE_REQ: [CommandHandler('close_request', close_request)]
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    # client_conv_handler = ConversationHandler(
        # entry_points=[CommandHandler("photo_handler",photo_handler)],
        # states={            
            # Message handler, then close chat, then feedback
    #     },
    #     fallbacks=[CommandHandler("cancel",cancel)],
    # )

    application.add_handler(admin_conv_handler)
    # application.add_handler(client_conv_handler)

    # user sending photo and creating request
    photo_handler = MessageHandler(filters.PHOTO, handle_photo)
    
    application.add_handler(start_handler)
    application.add_handler(photo_handler)
    application.add_handler(register_handler)

    application.add_error_handler(error_handler)


    # chat
    application.add_handler(CallbackQueryHandler(callback_query_handler))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), message_handler))

    application.run_polling()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())

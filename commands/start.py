from telegram import Update, ReplyKeyboardRemove
from telegram.ext import CallbackContext, CommandHandler
from database.connection import connect_to_db
import logging
import psycopg2

logger = logging.getLogger(__name__)

async def start(update: Update, context: CallbackContext) -> None:
    user_id = update.effective_chat.id

    connection = connect_to_db()
    if not connection:
        await update.message.reply_text("Error with connection to DB /start.")
        return

    try:
        cursor = connection.cursor()
        cursor.execute("SELECT phone_number FROM Clients WHERE client_id = %s", (user_id,))
        user = cursor.fetchone()

        if user:
            cursor.execute("SELECT admin_id FROM Admins WHERE admin_id = %s", (user_id,))
            admin = cursor.fetchone()

            if admin:
                await update.message.reply_text(
                    "Available commands /get_requests, /another_command",
                    reply_markup=ReplyKeyboardRemove(),
                )
            else:
                await update.message.reply_text(
                    "You can /submit_request",
                    reply_markup=ReplyKeyboardRemove(),
                )
        else:
            await update.message.reply_text(
                "/register <phone number>.",
                reply_markup=ReplyKeyboardRemove(),
            )

    except (Exception, psycopg2.Error) as error:
        logger.error("Error with DB /start: %s", error)
        await update.message.reply_text("Error /start.")
    finally:
        if connection:
            connection.close()
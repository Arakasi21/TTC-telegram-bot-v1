from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import CallbackContext
from database.connection import connect_to_db
import logging
import psycopg2

logger = logging.getLogger(__name__)

async def start(update: Update, context: CallbackContext) -> None:
    user_id = update.effective_chat.id

    client_keyboard = [['/submit_request', 'check status command v buduwem']]
    admin_keyboard = [['/get_requests', 'Potom che nit budet']]

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
                    "Welcome, Admin! Commands are available:",
                    reply_markup=ReplyKeyboardMarkup(admin_keyboard, one_time_keyboard=True, resize_keyboard=True),
                )
            else:
                await update.message.reply_text(
                    "Welcome!",
                    reply_markup=ReplyKeyboardMarkup(client_keyboard, one_time_keyboard=True, resize_keyboard=True),
                )
        else:
            await update.message.reply_text(
                "Please /register with your <phone number>.",
                reply_markup=ReplyKeyboardMarkup([['Register']], one_time_keyboard=True, resize_keyboard=True),
            )

    except (Exception, psycopg2.Error) as error:
        logger.error("Error with DB /start: %s", error)
        await update.message.reply_text("Error /start.")
    finally:
        if connection:
            connection.close()
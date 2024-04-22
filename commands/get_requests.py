from database.connection import connect_to_db
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from settings.constants import TAKE_REQ
import logging

logger = logging.getLogger(__name__)


async def get_requests(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_id = update.effective_chat.id
    admin_id = 577163143  # потом заменю

    if user_id != admin_id:
        await context.bot.send_message(chat_id=user_id, text="No access!")
        return

    connection = connect_to_db()
    if not connection:
        await context.bot.send_message(chat_id=user_id, text="Error with connection to db.")
        return

    try:
        cursor = connection.cursor()
        cursor.execute("SELECT request_id, status, problem_description FROM Requests WHERE status = 'New' OR status = 'Pending'")
        rows = cursor.fetchall()

        keyboard = [[InlineKeyboardButton(f"Request ID: {row[0]}, Status: {row[1]}, Problem: {row[2]}", callback_data=f"take_{row[0]}")]
                    for row in rows]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text('Please select a request:', reply_markup=reply_markup)

    except Exception as e:
        logger.error(f"Error with getting list of requests: {e}")
        await context.bot.send_message(chat_id=user_id, text="Error with getting list of requests.")
    finally:
        if connection:
            connection.close()

    return TAKE_REQ

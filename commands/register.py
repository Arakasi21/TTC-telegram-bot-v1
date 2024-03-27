from telegram import Update
from telegram.ext import CallbackContext
from database.connection import connect_to_db
import logging
import psycopg2

logger = logging.getLogger(__name__)

async def register(update: Update, context: CallbackContext) -> None:
    if len(context.args) != 1:
        await update.message.reply_text("/register <phone number>")
        return

    phone_number = context.args[0]
    user_id = update.effective_chat.id

    connection = connect_to_db()
    if not connection:
        await update.message.reply_text("Error with connection to DB /register.")
        return

    try:
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO Clients (client_id, phone_number) VALUES (%s, %s) ON CONFLICT (client_id) DO NOTHING",
            (user_id, phone_number,)
        )
        connection.commit()
        await update.message.reply_text("Success in registration")

    except (Exception, psycopg2.Error) as error:
        logger.error("Error with register: %s", error)
        await update.message.reply_text("Error with register.")
    finally:
        if connection:
            connection.close()
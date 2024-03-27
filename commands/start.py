from database.connection import connect_to_db
import logging
import psycopg2

logger = logging.getLogger(__name__)

async def start(update, context):
    user_id = update.effective_chat.id
    phone_number = +77089380726

    if not phone_number:
        await context.bot.send_message(chat_id=user_id, text="Number:")
        return

    connection = connect_to_db()
    if connection:
        cursor = connection.cursor()
        try:
            cursor.execute("INSERT INTO Clients (client_id, phone_number) VALUES (%s, %s)", (user_id, phone_number,))
            connection.commit()
            await context.bot.send_message(chat_id=user_id, text="Success!")
        except (Exception, psycopg2.Error) as error:
            logger.error("Error registering user: %s", error)
            await context.bot.send_message(chat_id=user_id, text="Error.")
        finally:
            connection.close()
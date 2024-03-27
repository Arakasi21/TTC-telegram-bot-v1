from database.connection import connect_to_db
import psycopg2
import logging

logger = logging.getLogger(__name__)

async def submit_request(update, context):
    user_id = update.effective_chat.id
    request_text = update.message.text

    connection = connect_to_db()
    if not connection:
        await context.bot.send_message(chat_id=user_id, text="Error connecting to database.")
        return
    try:
        cursor = connection.cursor()
        cursor.execute("INSERT INTO Requests (client_id, timestamp, status, request_text) VALUES (%s, now(), %s, %s)", (user_id, "New", request_text))
        connection.commit()
        await context.bot.send_message(chat_id=user_id, text="Request success!")
    except (Exception, psycopg2.Error) as error:
        logger.error("Error submitting request: %s", error)
        await context.bot.send_message(chat_id=user_id, text="Error.")
    finally:
        if connection:
            connection.close()
from telegram.error import BadRequest
from database.connection import connect_to_db
import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import os

logger = logging.getLogger(__name__)

async def take_request(update, context):
    user_id = update.effective_chat.id
    admin_id = 577163143  # переделать
    
    if user_id != admin_id:
        await context.bot.send_message(chat_id=user_id, text="No access!")
        return

    if len(context.args) != 1:
        await update.message.reply_text("Usage: /take_request <request_id>")
        return
    
    request_id = context.args[0]

    connection = connect_to_db()
    if not connection:
        await context.bot.send_message(chat_id=user_id, text="Error with connection to db.")
        return
    try:
        cursor = connection.cursor()
        # мы получаем photo_path 
        cursor.execute("SELECT photo_id, client_id FROM Requests WHERE request_id = %s", (request_id,))
        result = cursor.fetchone()

        if result:
            photo_info, client_id = result
            print(photo_info)
        else:
            logger.error("Request not found.")
            await context.bot.send_message(chat_id=admin_id, text="Запрос не найден.")
            return
        # photo_info, client_id = result if result else (None, None)
        # обновляем статус
        cursor.execute("UPDATE Requests SET status = 'In process', admin_id = %s WHERE request_id = %s", (user_id, request_id))
        connection.commit()
        if client_id:
            await context.bot.send_message(chat_id=client_id, text="Ваш запрос принят в обработку.")

        if photo_info and photo_info[0]:
            photo_path = photo_info
            logger.info(f"Photo path: {photo_path}")
            logger.info(f"Client id: {client_id}")
            os.getcwd()
            
            try:
                if photo_path.startswith("http"):
                    await context.bot.send_message(chat_id=admin_id, text=f"Photo URL: {photo_path}")
                else:
                    with open(photo_path, 'rb') as photo:
                        await context.bot.send_photo(chat_id=admin_id, photo=photo)
            except BadRequest as e:
                logger.error(f"Error sending photo to admin: {e}")
                await context.bot.send_message(chat_id=admin_id, text="Error sending photo.")
        else:
            await context.bot.send_message(chat_id=admin_id, text="No photo associated with this request.")

        await context.bot.send_message(chat_id=admin_id, text=f"Запрос {request_id} теперь отмечен как 'In process' и взят вами.")
        
        if client_id:
            keyboard = [[InlineKeyboardButton("Начать чат", callback_data=f"chat_{client_id}")]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await context.bot.send_message(chat_id=admin_id, text="Нажмите кнопку ниже, чтобы начать чат с клиентом.", reply_markup=reply_markup)
    
    except Exception as e:
        logger.error(f"Error updating request status or fetching photo: {e}")
        await context.bot.send_message(chat_id=user_id, text="Error updating request status or fetching photo.")
    finally:
        if connection:
            cursor.close()
            connection.close()
from telegram.ext import CallbackContext
from telegram import Update
from database.connection import connect_to_db
import uuid
import os

async def handle_photo(update: Update, context: CallbackContext):
    photo_file = update.message.photo[-1]

    client_id = update.message.from_user.id
    photo_number = str(uuid.uuid4())
    photo_name = f"{client_id}_{photo_number}.jpg"

    temp_photo_dir = "./temp_photos"
    temp_photo_path = os.path.join(temp_photo_dir, photo_name)

    if not os.path.exists(temp_photo_dir):
        os.makedirs(temp_photo_dir)

    try:
        telegram_file = await photo_file.get_file()
        await telegram_file.download_to_drive(temp_photo_path) 
        
        await save_photo_path_in_database(client_id, temp_photo_path)
        await update.message.reply_text("Фотография сохранена и Request отправлен.")

        #пока локально сохраняется - не буду удалять фото из /temp. Если в будущем нужно будет сохранять где то - то просто 

         # server_drive_path = await upload_to_server_drive(temp_photo_path, photo_name)

          # await save_photo_path_in_database(client_id, server_drive_path)

        # os.remove(temp_photo_path)

    except AttributeError:
        print("Warning: Telegram library version might not support 'download' method.")


async def save_photo_path_in_database(client_id, photo_path):
    conn = connect_to_db() 
    if conn is not None:
        try:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO Requests (client_id, photo_id, timestamp, status) VALUES (%s, %s, CURRENT_TIMESTAMP, 'New')", (client_id, photo_path))
            conn.commit()
        except (Exception, psycopg2.Error) as error:
            print(f"Error while inserting into database: {error}")
        finally:
            cursor.close()
            conn.close()
    else:
        print("Failed to connect to database.")
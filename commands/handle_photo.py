from telegram.ext import CallbackContext
from telegram import Update
import uuid

async def handle_photo(update: Update, context: CallbackContext):
    photo_file = update.message.photo[-1].get_file()
    client_id = update.message.from_user.id
    photo_number = str(uuid.uuid4())
    photo_name = f"{client_id}_{photo_number}.jpg"
    
    temp_photo_path = f"./temp/{photo_name}"
    await photo_file.download(temp_photo_path)
    
    google_drive_path = await upload_to_google_drive(temp_photo_path, photo_name)
    await save_photo_path_in_database(client_id, google_drive_path)
    
    await update.message.reply_text("Your photo has been saved.")
    
    os.remove(temp_photo_path)

def upload_to_google_drive(photo_path, photo_name):
    pass

def save_photo_path_in_database(client_id, google_drive_path):
    pass

from telegram.ext import CallbackContext
from telegram import Update
from database.connection import connect_to_db
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
# from settings.config import GOOGLE_CREDENTIALS_PATH
import uuid
import os

async def handle_photo(update: Update, context: CallbackContext):
  photo_file = update.message.photo[-1]  # Get the last photo in the message

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
    
  except AttributeError:
    print("Warning: Telegram library version might not support 'download' method.")

  google_drive_path = await upload_to_google_drive(temp_photo_path, photo_name)

  await save_photo_path_in_database(client_id, google_drive_path)

  await update.message.reply_text("Your photo has been saved.")

  os.remove(temp_photo_dir)


def upload_to_google_drive(photo_path, photo_name):
    SCOPES = ['https://www.googleapis.com/auth/drive']
    creds = None

    flow = InstalledAppFlow.from_client_secrets_file("client_secret_356701748025-e6seoun4pra6tcvbsfq5k7783aap018s.apps.googleusercontent.com.json", SCOPES)
    creds = flow.run_local_server(port=0)

    service = build('drive', 'v3', credentials=creds)

    file_metadata = {'name': photo_name}
    media = MediaFileUpload(photo_path, mimetype='image/jpeg')
    file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    
    print(f"Uploaded file ID: {file.get('id')}")
    return file.get('id')


def save_photo_path_in_database(client_id, google_drive_path):
    conn = connect_to_db() 
    if conn is not None:
        try:
            cursor = conn.cursor()
            query = """INSERT INTO Requests (client_id, google_drive_path) VALUES (%s, %s)"""
            cursor.execute(query, (client_id, google_drive_path))
            conn.commit()
            logger.info("Path saved in database.")
        except (Exception, psycopg2.Error) as error:
            logger.error("Error while inserting into database: %s", error)
        finally:
            cursor.close()
            conn.close()
    else:
        logger.error("Failed to connect to database.")
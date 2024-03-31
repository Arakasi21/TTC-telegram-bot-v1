import os
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv()

# Database settings
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_DATABASE = os.getenv('DB_DATABASE')
DB_HOST = os.getenv('DB_HOST')
DB_URL = os.getenv('DB_URL')

# Google Drive API Key
# google_credentials_string = os.getenv('GOOGLE_CREDENTIALS')
# GOOGLE_API_KEY_JSON = json.loads(google_credentials_string)


# GOOGLE_CREDENTIALS_PATH = os.getenv('GOOGLE_CREDENTIALS_PATH')

# if GOOGLE_CREDENTIALS_PATH is None:
#     raise ValueError("Missing environment variable: GOOGLE_CREDENTIALS_PATH")
    
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

# Telegram Bot Token
TOKEN = os.getenv('TOKEN')
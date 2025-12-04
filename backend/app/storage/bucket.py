import os
from dotenv import load_dotenv
import firebase_admin
from firebase_admin import credentials, storage

# Load environment variables
load_dotenv()

CREDENTIALS_FILE = os.getenv("GOOGLE_APPLICATION_CREDENTIALS", "serviceAccountKey.json")
GCP_BUCKET_NAME = os.getenv("GCP_STORAGE_BUCKET")

if not GCP_BUCKET_NAME:
    raise ValueError("GCP_STORAGE_BUCKET is not set in .env!")

# Prevent double initialization
if not firebase_admin._apps:
    cred = credentials.Certificate(CREDENTIALS_FILE)
    firebase_admin.initialize_app(cred, {"storageBucket": GCP_BUCKET_NAME})

# Always specify bucket name explicitly
bucket = storage.bucket(GCP_BUCKET_NAME)

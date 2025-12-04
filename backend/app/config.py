import os
from dotenv import load_dotenv

load_dotenv()

FRONTEND_ORIGIN = os.getenv("FRONTEND_ORIGIN", "http://localhost:5173")
GCP_BUCKET_NAME = os.getenv("GCP_STORAGE_BUCKET", "file-upload-app-bucket")
CREDENTIALS_FILE = os.getenv("GOOGLE_APPLICATION_CREDENTIALS", "serviceAccountKey.json")

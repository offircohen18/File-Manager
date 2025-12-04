import os
from dotenv import load_dotenv
import firebase_admin
from firebase_admin import credentials, storage

load_dotenv()

def init_firebase():
    if not firebase_admin._apps:
        cred = credentials.Certificate("serviceAccountKey.json")
        bucket_name = os.getenv("GCP_STORAGE_BUCKET")
        if not bucket_name:
            raise ValueError("GCP_STORAGE_BUCKET is not set in env!")
        firebase_admin.initialize_app(cred, {"storageBucket": bucket_name})

def get_bucket():
    init_firebase()
    return storage.bucket()

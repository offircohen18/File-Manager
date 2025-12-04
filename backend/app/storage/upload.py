import datetime
from app.storage.bucket import bucket

def upload_file(file, uid):
    blob_name = f"{uid}/{file.filename}"
    blob = bucket.blob(blob_name)

    blob.metadata = {
        "user_id": uid,
        "original_filename": file.filename,
        "content_type": file.content_type,
        "created_at": datetime.datetime.utcnow().isoformat()
    }

    blob.upload_from_file(file.file, content_type=file.content_type)

    return {
        "filename": file.filename,
        "blob_name": blob_name
    }

import datetime
from pathlib import Path
from app.storage.bucket import bucket

def upload_file(file, uid):
    blob_name = f"{uid}/{file.filename}"
    blob = bucket.blob(blob_name)

    created_at = datetime.datetime.utcnow().isoformat()
    content_type = file.content_type

    blob.metadata = {
        "user_id": uid,
        "original_filename": file.filename,
        "content_type": content_type,
        "created_at": created_at
    }

    blob.upload_from_file(file.file, content_type=content_type)

    return {
        "filename": file.filename,
        "blob_name": blob_name,
        "size": blob.size,
        "content_type": content_type,
        "created_at": created_at,
        "user_id": uid
    }

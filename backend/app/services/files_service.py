import os
from pathlib import Path
from fastapi import HTTPException
from fastapi.responses import FileResponse
from typing import List, Optional
from app.models import FileResponseModel, UploadFilesResponse
from app.storage.upload import upload_file
from app.storage.bucket import bucket

ALLOWED_EXTENSIONS = {".json", ".txt", ".pdf"}

def check_permission(token: dict, blob_user_id: str):
    if token.get("role", "user") != "admin" and blob_user_id != token["uid"]:
        raise HTTPException(status_code=403, detail="Unauthorized")

async def upload_files_service(files: list, token: dict) -> UploadFilesResponse:
    uid = token["uid"]
    uploaded = []

    for file in files:
        _, ext = os.path.splitext(file.filename)
        if ext.lower() not in ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=400,
                detail=f"File type '{ext}' not allowed. Allowed: {', '.join(ALLOWED_EXTENSIONS)}"
            )
        uploaded.append(upload_file(file, uid))

    return UploadFilesResponse(
        message="Files uploaded successfully",
        files=[FileResponseModel(**f) for f in uploaded]
    )

async def list_files_service(token: dict, sort_by: Optional[str], file_type: Optional[str], search: Optional[str]) -> List[FileResponseModel]:
    uid = token["uid"]
    user_role = token.get("role", "user")

    blobs = list(bucket.list_blobs())
    files = []

    for blob in blobs:
        blob.reload()
        meta = blob.metadata or {}

        if user_role != "admin" and meta.get("user_id") != uid:
            continue

        filename = meta.get("original_filename", blob.name)

        if file_type and not filename.lower().endswith(file_type.lower()):
            continue
        if search and search.lower() not in filename.lower():
            continue

        files.append(FileResponseModel(
            filename=filename,
            blob_name=blob.name,
            size=blob.size,
            content_type=meta.get("content_type"),
            created_at=meta.get("created_at"),
            user_id=meta.get("user_id")
        ))

    if sort_by == "date":
        files.sort(key=lambda x: x.created_at or "", reverse=True)
    elif sort_by == "size":
        files.sort(key=lambda x: x.size or 0, reverse=True)

    return files

async def download_file_service(blob_name: str, token: dict) -> FileResponse:
    safe_name = Path(blob_name).name
    blob = bucket.blob(blob_name)
    blob.reload()

    if not blob.exists():
        raise HTTPException(status_code=404, detail="File not found")

    meta = blob.metadata or {}
    check_permission(token, meta.get("user_id", ""))

    tmp_path = os.path.join("/tmp", safe_name)
    os.makedirs(os.path.dirname(tmp_path), exist_ok=True)
    blob.download_to_filename(tmp_path)

    filename = meta.get("original_filename", safe_name)
    return FileResponse(tmp_path, filename=filename)

async def delete_file_service(blob_name: str, token: dict):
    blob = bucket.blob(blob_name)
    blob.reload()

    if not blob.exists():
        raise HTTPException(status_code=404, detail="File not found")

    meta = blob.metadata or {}
    check_permission(token, meta.get("user_id", ""))

    blob.delete()
    return {"message": "File deleted successfully"}

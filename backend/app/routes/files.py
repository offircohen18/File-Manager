from fastapi import APIRouter, Depends, UploadFile, File, Query
from typing import List, Optional

from app.auth.verify_token import verify_token
from app.handlers.files_handler import (
    upload_handler,
    list_files_handler,
    download_handler,
    delete_handler
)

router = APIRouter()

@router.post("/upload")
async def upload_files(
    files: List[UploadFile] = File(...),
    token: dict = Depends(verify_token)
):
    return await upload_handler(files, token)


@router.get("/files")
async def list_files(
    token: dict = Depends(verify_token),
    sort_by: Optional[str] = Query(None),
    file_type: Optional[str] = Query(None),
    search: Optional[str] = Query(None)
):
    return await list_files_handler(token, sort_by, file_type, search)


@router.get("/download/{blob_name:path}")
async def download_file(blob_name: str, token: dict = Depends(verify_token)):
    return await download_handler(blob_name, token)


@router.delete("/delete/{blob_name:path}")
async def delete_file(blob_name: str, token: dict = Depends(verify_token)):
    return await delete_handler(blob_name, token)

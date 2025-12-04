from fastapi.responses import FileResponse
from fastapi import UploadFile

from app.services.files_service import (
    upload_files_service,
    list_files_service,
    download_file_service,
    delete_file_service
)

async def upload_handler(files: list[UploadFile], token: dict):
    return await upload_files_service(files, token)


async def list_files_handler(token: dict, sort_by: str, file_type: str, search: str):
    return await list_files_service(token, sort_by, file_type, search)


async def download_handler(blob_name: str, token: dict):
    return await download_file_service(blob_name, token)


async def delete_handler(blob_name: str, token: dict):
    return await delete_file_service(blob_name, token)

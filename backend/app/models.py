from pydantic import BaseModel
from typing import Optional, List

class FileResponseModel(BaseModel):
    filename: str
    blob_name: str
    size: int
    content_type: Optional[str]
    created_at: Optional[str]
    user_id: Optional[str]

class UploadFilesResponse(BaseModel):
    message: str
    files: List[FileResponseModel]

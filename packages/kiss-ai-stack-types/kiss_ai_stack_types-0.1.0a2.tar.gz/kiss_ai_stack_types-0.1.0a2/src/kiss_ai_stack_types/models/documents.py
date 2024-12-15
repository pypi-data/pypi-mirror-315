from typing import List, Dict, Any, Optional

from pydantic import BaseModel, Field


class FileObject(BaseModel):
    name: str = Field('', description='File name')
    content: Any = Field(None, description='Base64-encoded file content')


class DocumentsRequestBody(BaseModel):
    """
    Structured request for document upload
    """
    files: List[FileObject] = Field(
        ...,
        description='List of files to upload. Each file is a dictionary with `name` and base64-encoded `content`'
    )
    metadata: Optional[Dict[str, Any]] = Field(
        None,
        description='Optional metadata for the upload'
    )

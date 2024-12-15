from typing import Optional
from pydantic import BaseModel, Field, field_validator

from kiss_ai_stack_types.enums import SessionScope


class SessionRequest(BaseModel):
    scope: Optional[SessionScope] = Field(None, description='Session scope, `temporary` or `persistent`')
    client_id: Optional[str] = Field(None, description='Client id from a previous session')
    client_secret: Optional[str] = Field(None, description='Matching client\'s secret')


class SessionResponse(BaseModel):
    client_id: str
    client_secret: str
    access_token: str

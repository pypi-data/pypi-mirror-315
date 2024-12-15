from typing import Any

from pydantic import BaseModel, Field


class GenericResponseBody(BaseModel):
    agent_id: str = Field('', description='Agent/client Id')
    result: Any = Field(None, description='Generated answer')
    extras: Any = Field(None, description='Other return values')

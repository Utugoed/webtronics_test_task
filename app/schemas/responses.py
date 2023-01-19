from typing import Optional
from pydantic import BaseModel, Field


class ResponseModel(BaseModel):
    OK: bool = Field(..., title="Operation was successfully completed")
    detail: Optional[str] = Field(None, title="Operation's failure detail")
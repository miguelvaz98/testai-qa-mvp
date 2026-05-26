from pydantic import BaseModel
from typing import Literal, Optional

class GenerateRequest(BaseModel):
    input: str
    framework: Literal["cypress", "playwright", "jest"] = "playwright"
    session_id: Optional[str] = None

class GenerateResponse(BaseModel):
    framework: str
    tests: str
    tokens_used: int

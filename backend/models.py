from pydantic import BaseModel
from typing import Literal

class GenerateRequest(BaseModel):
    input: str  # frontend code or user story
    framework: Literal["cypress", "playwright", "jest"] = "playwright"

class GenerateResponse(BaseModel):
    framework: str
    tests: str
    tokens_used: int

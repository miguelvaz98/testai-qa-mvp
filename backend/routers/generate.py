from fastapi import APIRouter, HTTPException
from backend.models import GenerateRequest, GenerateResponse
from backend.services.llm import generate_tests

router = APIRouter()

@router.post("/generate", response_model=GenerateResponse)
def generate(req: GenerateRequest):
    if not req.input.strip():
        raise HTTPException(status_code=400, detail="Input cannot be empty.")
    tests, tokens = generate_tests(req.input, req.framework)
    return GenerateResponse(framework=req.framework, tests=tests, tokens_used=tokens)

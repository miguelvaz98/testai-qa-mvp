from fastapi import APIRouter, HTTPException
from backend.models import GenerateRequest, GenerateResponse
from backend.services.llm import generate_tests
from backend.services.trials import is_allowed, increment

router = APIRouter()

@router.post("/generate", response_model=GenerateResponse)
def generate(req: GenerateRequest):
    if not req.input.strip():
        raise HTTPException(status_code=400, detail="Input cannot be empty.")

    if req.session_id:
        if not is_allowed(req.session_id):
            raise HTTPException(status_code=402, detail="Free trial exhausted. Upgrade to continue.")

    tests, tokens = generate_tests(req.input, req.framework)

    if req.session_id:
        increment(req.session_id)

    return GenerateResponse(framework=req.framework, tests=tests, tokens_used=tokens)

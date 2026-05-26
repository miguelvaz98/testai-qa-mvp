from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.routers.generate import router

app = FastAPI(title="TestAI-QA API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["POST"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api")

@app.get("/health")
def health():
    return {"status": "ok"}

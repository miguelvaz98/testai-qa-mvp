from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.routers.generate import router
from backend.routers.checkout import router as checkout_router
from backend.routers.webhook import router as webhook_router

app = FastAPI(title="TestAI-QA API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api")
app.include_router(checkout_router, prefix="/api")
app.include_router(webhook_router, prefix="/api")

@app.get("/health")
def health():
    return {"status": "ok"}

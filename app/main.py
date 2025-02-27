from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from app.routes import router
from app.config import settings
from app.logging import logger
from app.model import Model
import uvicorn

app = FastAPI(
    title="qwen-25-api", 
    description="Use this API for inferencing with Qwen2.5-0.5B-Instruct model.", 
    version="1.0"
    )

@app.on_event("startup")
async def load_model_on_startup():
    """Ensures the model is preloaded at startup."""
    logger.info("Loading model and tokenizer at startup...")
    Model()  # This ensures the singleton instance is created
    logger.info("Model and tokenizer loaded successfully at startup.")

# Enable CORS Middleware with Restricted POST method
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,  # Allowed origins (update in production)
    allow_methods=settings.ALLOWED_METHODS,  # Restrict to POST only
    allow_headers=settings.ALLOWED_HEADERS,  # Allow specified headers
    allow_credentials=settings.ALLOWED_CREDENTIALS  # Enable credentials (if authentication is required)
)

# Include API routes
app.include_router(router)

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, workers=4)

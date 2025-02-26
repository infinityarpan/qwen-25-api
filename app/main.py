from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from app.routes import router
from app.config import settings
import uvicorn

app = FastAPI(
    title="qwen-25-api", 
    description="Use this API for inferencing with Qwen2.5-0.5B-Instruct model.", 
    version="1.0"
    )

# Enable CORS Middleware with Restricted POST method
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,  # Allow all or specific domains
    allow_methods=settings.ALLOWED_METHODS,  # Restrict to POST only
    allow_headers=settings.ALLOWED_HEADERS,
    allow_credentials=True,  # Enable if using authentication
)

# Include API routes
app.include_router(router)

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, workers=4)

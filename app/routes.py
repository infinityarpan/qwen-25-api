import time
from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from typing import Any
from app.model import Model
from app.utils import generate_response
from app.config import settings


# API Router
router = APIRouter(
    prefix=settings.API_PREFIX,  # Base path for all endpoints
    tags=settings.API_TAGS,  # Organize routes by feature
)

# Request Schema
class RequestBody(BaseModel):
    prompt: str = Field(..., description="User input prompt")

# Model Dependency
def get_model():
    model_client = Model()
    return model_client.model, model_client.tokenizer, model_client.model_name

@router.post("/generate")
async def generate_text(request: RequestBody, model_data: Any = Depends(get_model)):
    model, tokenizer, model_name = model_data
    return generate_response(model, tokenizer, model_name, request)

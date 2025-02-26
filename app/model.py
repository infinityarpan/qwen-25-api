from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
import os
from app.config import settings

class Model:
    """A model class to load the model and tokenizer efficiently with caching"""

    def __init__(self) -> None:
        self.model_name = settings.MODEL_NAME
        self.model_path = settings.MODEL_PATH
        
        # Check if the model directory exists
        if not os.path.exists(self.model_path):
            raise FileNotFoundError(f"Model directory not found: {self.model_path}")

        # Initialize attributes for caching
        self._model = None
        self._tokenizer = None

    def load_model(self):
        """Lazy loads the model only once to optimize performance"""
        if self._model is None:  # Load only if not already loaded
            try:
                self._model = AutoModelForCausalLM.from_pretrained(
                    self.model_path,
                    torch_dtype=torch.float16,  # Optimize memory usage
                    device_map="auto",
                    trust_remote_code=True
                )
            except Exception as e:
                raise RuntimeError(f"Error loading model: {e}")
        return self._model

    def load_tokenizer(self):
        """Lazy loads the tokenizer only once"""
        if self._tokenizer is None:
            try:
                self._tokenizer = AutoTokenizer.from_pretrained(self.model_path, trust_remote_code=True)
            except Exception as e:
                raise RuntimeError(f"Error loading tokenizer: {e}")
        return self._tokenizer

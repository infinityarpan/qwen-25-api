from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
import os
from app.config import settings
from app.logging import logger

class SingletonMeta(type):
    """Thread-safe Singleton Metaclass."""
    _instances = {}

    def __call__(cls, *args, **kwargs):
        """Ensures only one instance of the class is created."""
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)  # Create new instance
            cls._instances[cls] = instance
        return cls._instances[cls]

class Model(metaclass=SingletonMeta):
    """A singleton class to efficiently load and cache the model and tokenizer."""

    def __init__(self):
        """Initialize model parameters and pre-load model and tokenizer."""
        self.model_name = settings.MODEL_NAME
        self.model_path = settings.MODEL_PATH

        if not os.path.exists(self.model_path):
            raise FileNotFoundError(f"Model directory not found: {self.model_path}")

        self.model = None
        self.tokenizer = None

        # Load model and tokenizer
        self._load_model()
        self._load_tokenizer()

    def _load_model(self):
        """Loads the model from the specified path."""
        try:
            self.model = AutoModelForCausalLM.from_pretrained(
                self.model_path,
                torch_dtype=torch.float16,  
                device_map="auto",
                trust_remote_code=True
            )
            logger.info("Model loaded successfully.")
        except Exception as e:
            logger.error(f"Error loading model: {e}")
            raise RuntimeError(f"Error loading model: {e}")

    def _load_tokenizer(self):
        """Loads the tokenizer from the specified path."""
        try:
            self.tokenizer = AutoTokenizer.from_pretrained(
                self.model_path, trust_remote_code=True
            )
            logger.info("Tokenizer loaded successfully.")
        except Exception as e:
            logger.error(f"Error loading tokenizer: {e}")
            raise RuntimeError(f"Error loading tokenizer: {e}")

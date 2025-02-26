import time
import torch
from fastapi import HTTPException
from app.logging import logger
from app.config import settings

def generate_response(model, tokenizer, model_name, request):
    """Handles text generation logic."""
    start_time = time.time()  # ✅ Moved this inside the function

    try:
        messages = [
            {"role": "system", "content": settings.SYSTEM_PROMPT},
            {"role": "user", "content": request.prompt}
        ]
        text = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)

        model_inputs = tokenizer([text], return_tensors="pt").to(model.device)
        input_token_count = model_inputs.input_ids.shape[1]  

        # Context length validation
        if input_token_count > settings.MAX_CONTEXT_LENGTH - settings.MAX_NEW_TOKENS:
            raise HTTPException(status_code=400, detail="Max context length exceeded")

        # Generate response
        with torch.no_grad():  # ✅ Disable gradients for inference efficiency
            generated_ids = model.generate(
                **model_inputs,
                max_new_tokens=settings.MAX_NEW_TOKENS,
                do_sample=settings.DO_SAMPLE,
                top_k=settings.TOP_K,
                top_p=settings.TOP_P,
                temperature=settings.TEMPERATURE
            )

        output_token_count = sum(len(ids) for ids in generated_ids)

        # Extract only generated tokens
        generated_ids = [output_ids[len(input_ids):] for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)]
        response = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]

        # Latency measurement
        latency = round((time.time() - start_time) * 1000, 2)

        # Logging
        logger.info(f"Model: {model_name}, Input Tokens: {input_token_count}, Output Tokens: {output_token_count}, Latency: {latency}ms")

        return {
            "response": response,
            "model": model_name,
            "input_tokens": input_token_count,
            "output_tokens": output_token_count,
            "temperature": settings.TEMPERATURE,
            "top_p": settings.TOP_P,
            "top_k": settings.TOP_K,
            "max_new_tokens": settings.MAX_NEW_TOKENS,
            "do_sample": settings.DO_SAMPLE,
            "latency_ms": latency
        }

    except Exception as e:
        logger.error(f"Error generating text: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

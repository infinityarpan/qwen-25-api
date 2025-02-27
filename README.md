# Qwen-2.5-API: A Fast API for the Qwen-2.5 Language Model

This project provides a RESTful API for interacting with the Qwen-2.5 language model. It's designed for easy deployment and efficient text generation, allowing you to leverage the power of Qwen-2.5 in your applications.

## Features

*   **Text Generation:** Generate coherent and context-aware text based on user prompts.
*   **Customizable Parameters:** Adjust generation parameters like `temperature`, `top_k`, `top_p`, and `max_new_tokens` to fine-tune the output.
*   **Context Handling:** Supports long context handling, up to the model's maximum context length.
*   **Logging:** Detailed logging of token counts, and latency for debugging and monitoring.
*   **FastAPI:** Built with FastAPI for speed and efficiency.
*   **Dependency Injection:** Uses FastAPI's dependency injection for clean and organized code.
*   **Configuration:**  Settings are managed through a `config.py` file and can be overridden using environment variables.
* **Clear Error Handling:** Implements clear error handling with appropriate HTTP status codes.
* **Model configuration Tracking:** Accurately tracks and returns the model name and configurations like top_k, top_p, temperature, max_new_tokens, etc.

## Project Structure

qwen-25-api/  
│── app/                     # Main application folder  
│   ├── config.py            # Configuration settings (constants, API keys, etc.)  
│   ├── logging.py           # Logging setup (logs API calls, errors, etc.)  
│   ├── model.py             # Model loading and management (loads Qwen model)  
│   ├── routes.py            # API endpoints (FastAPI/Flask routes to interact with the model)  
│   └── utils.py             # Helper functions (text preprocessing, response formatting, etc.)  
│── models/                  # Local Model Storage  
│   └── Qwen2.5-0.5B-Instruct/  # Model-specific directory  
│       ├── added_tokens.json  
│       ├── config.json  
│       ├── generation_config.json  
│       ├── merges.txt  
│       ├── model.safetensors  # Pre-trained model weights  
│       ├── special_tokens_map.json  
│       ├── tokenizer_config.json  
│       ├── tokenizer.json  
│       └── vocab.json  
│── main.py                  # Entry point for running the API  
│── .env                     # Stores environment variables (optional, for API keys, secrets, etc.)  
│── requirements.txt         # Dependencies for the project  
│── README.md                # Documentation about the project


## Setup and Installation

## Option 1:

1.  **Clone the Repository:**

    ```bash
    git clone https://github.com/infinityarpan/qwen-25-api.git
    cd qwen-25-api
    ```

2. **Running the Application with Docker Compose**

    ```bash
    docker compose up --build -d
    ```

## Option 2:

1.  **Clone the Repository:**

    ```bash
    git clone https://github.com/infinityarpan/qwen-25-api.git
    cd qwen-25-api
    ```

2.  **Install Dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

3.  **Download the Qwen-2.5 Model: (Optional)**
    This repository already includes the Qwen-2.5 model weights and configurations. However, if you prefer to download the model directly from Hugging Face, you can run the download_model.ipynb notebook. Running this notebook will automatically create the required directory structure.

4.  **Environment Variables (Optional):**
    *   Create a `.env` file in the root directory to override the default settings in `app/config.py`.
    *   Example `.env` content:

        ```
        MODEL_NAME="Qwen-2.5-1.8B-Instruct"
        MODEL_PATH="app/models/Qwen2.5-1.8B-Instruct"
        MAX_NEW_TOKENS=1024
        ```

## Running the API

1.  **Start the API:**

    ```bash
    uvicorn app.main:app --reload
    ```

2.  **Access the API:**

    *   The API will be running at `http://127.0.0.1:8000` by default.
    *   You can view the API documentation (Swagger UI) at `http://127.0.0.1:8000/docs`.

## Using the API

The API provides a single endpoint for generating text:

*   **Endpoint:** `/generate`
*   **Method:** `POST`
*   **Request Body:**

    ```json
    {
        "prompt": "What is the capital of France?"
    }
    ```

*   **Response Body:**

    ```json
    {
        "response": "The capital of France is Paris.",
        "model": "Qwen-2.5-0.5B-Instruct",
        "input_tokens": 8,
        "output_tokens": 7,
        "temperature": 0.7,
        "top_p": 0.9,
        "top_k": 50,
        "max_new_tokens": 512,
        "do_sample": true,
        "latency_ms": 150.32
    }
    ```
* **Error Handling**
    * If an error occurs during generation (e.g., context length exceeded or internal server error), the API will return a suitable HTTP error status code (400 or 500) with a corresponding error detail.

## Configuration

The application's behavior can be customized through the `config.py` file or by using environment variables. Key configuration options include:

*   **`MODEL_NAME`:** The name of the Qwen-2.5 model being used.
*   **`SYSTEM_PROMPT`:** The default system prompt sent to the model to guide responses.
*   **`MAX_NEW_TOKENS`:** The maximum number of tokens to generate in a response.
*   **`DO_SAMPLE`:** Whether to use sampling during generation.
*   **`TOP_K`:** The number of highest probability vocabulary tokens to keep for top-k-filtering.
*   **`TOP_P`:** The cumulative probability of parameter highest probability tokens to keep for nucleus sampling.
*   **`TEMPERATURE`:** The temperature for generation (higher values -> more randomness).
*   **`LOG_LEVEL`**: the level of logging

## Contributing

Contributions are welcome! If you have any suggestions, bug reports, or feature requests, please open an issue or submit a pull request.

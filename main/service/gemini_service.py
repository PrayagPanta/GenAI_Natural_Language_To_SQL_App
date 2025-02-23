import json
import os

import httpx
from dotenv import load_dotenv
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential


MODEL_NAME = "gemini-2.0-flash"
load_dotenv()

@retry(
    retry=retry_if_exception_type((httpx.RequestError, httpx.TimeoutException, httpx.HTTPStatusError)),
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=10),
    reraise=True
)
async def make_http_request_to_gemini(prompt: dict) -> dict:
    """
    Sends an asynchronous HTTP POST request to the Gemini API with retry logic.
    The prompt is wrapped inside a JSON request and the response JSON is returned.
    """
    request_body = {
        "contents": [{
            "parts": [{"text": json.dumps(prompt)}]
        }]
    }
    gemini_api = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL_NAME}:generateContent"
    gemini_api_key = os.getenv("GEMINI_API_KEY")
    async with httpx.AsyncClient(timeout=httpx.Timeout(30)) as client:
        response = await client.post(
            url=f"{gemini_api}?key={gemini_api_key}",
            json=request_body
        )
        response.raise_for_status()
        return response.json()

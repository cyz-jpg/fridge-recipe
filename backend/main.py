import base64
import logging
import os

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from fastapi.requests import Request
from dotenv import load_dotenv
from openai import OpenAI, OpenAIError

app = FastAPI()
load_dotenv()
logger = logging.getLogger(__name__)

MAX_IMAGE_SIZE = 5 * 1024 * 1024
ALLOWED_IMAGE_TYPES = {
    "image/jpeg",
    "image/png",
    "image/webp",
    "image/gif",
}


def get_openai_client() -> OpenAI:
    if not os.getenv("OPENAI_API_KEY"):
        raise HTTPException(status_code=500, detail="OpenAI API key is not configured.")
    return OpenAI()


async def read_limited_upload(file: UploadFile, max_size: int) -> bytes:
    data = await file.read(max_size + 1)
    if len(data) > max_size:
        raise HTTPException(status_code=413, detail="Image is too large. Maximum size is 5 MB.")
    if not data:
        raise HTTPException(status_code=400, detail="Uploaded image is empty.")
    return data


def detect_image_type(image_bytes: bytes) -> str | None:
    if image_bytes.startswith(b"\xff\xd8\xff"):
        return "image/jpeg"
    if image_bytes.startswith(b"\x89PNG\r\n\x1a\n"):
        return "image/png"
    if image_bytes.startswith((b"GIF87a", b"GIF89a")):
        return "image/gif"
    if len(image_bytes) >= 12 and image_bytes[:4] == b"RIFF" and image_bytes[8:12] == b"WEBP":
        return "image/webp"
    return None

@app.get("/")
def root():
    return {
        "message": "Fridge Recipe API is running"
    }

@app.post("/")
async def get_recommendations(image: UploadFile = File(...)):
    if image.content_type not in ALLOWED_IMAGE_TYPES:
        raise HTTPException(status_code=400, detail="Invalid image file. Please upload a valid image.")

    image_bytes = await read_limited_upload(image, MAX_IMAGE_SIZE)
    detected_type = detect_image_type(image_bytes)
    if detected_type is None or detected_type != image.content_type:
        raise HTTPException(status_code=400, detail="Invalid image file. Please upload a valid image.")

    base64_image = base64.b64encode(image_bytes).decode("utf-8")
    openai_client = get_openai_client()

    try:
        response = openai_client.responses.create(
            model="gpt-5.5",
            input=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "input_text",
                            "text": "Look at the image and provide a list of ingredients based on the items you recognize in the image."
                        },
                        {
                            "type": "input_image",
                            "image_url": f"data:{detected_type};base64,{base64_image}"
                        }
                    ]
                }
            ]
        )
    except OpenAIError as exc:
        logger.exception("OpenAI request failed")
        raise HTTPException(status_code=502, detail="Could not get a response from OpenAI.") from exc

    return {
        "recommendations": response.output_text
    }

@app.exception_handler(404)
async def not_found_handler(request: Request, exc):
    return JSONResponse(
        status_code=404,
        content={
            "error": "Not Found",
            "message": f"The route '{request.url.path}' does not exist.",
        }
    )

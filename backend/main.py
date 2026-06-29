from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.requests import Request

app = FastAPI()


@app.get("/")
def root():
    return {
        "message": "Fridge Recipe API is running"
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
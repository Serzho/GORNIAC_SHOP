import sys

sys.path.append("../../../backend")

from fastapi.responses import HTMLResponse
from backend.core.sevice import upload_pages
from fastapi import FastAPI

pages_dict = upload_pages()
app = FastAPI()


@app.get("/test")
async def test() -> dict:
    return {"Request": "success"}


@app.get("/", response_class=HTMLResponse)
async def main_page() -> HTMLResponse:
    page = pages_dict.get("index.html")
    if page is None:
        raise FileNotFoundError("index.html not found!")
    else:
        return HTMLResponse(content=page, status_code=200)


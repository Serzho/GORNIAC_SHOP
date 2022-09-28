import sys

sys.path.append("../../backend")

from core.database_handler import DatabaseHandler
from fastapi.responses import HTMLResponse
from core.sevice import upload_pages
from fastapi import FastAPI

sys.path.append("../../core")
pages_dict = upload_pages()
databaseHandler = DatabaseHandler()
app = FastAPI()

@app.get("/test")
async def test() -> dict:
    databaseHandler.signUp("aaaa", "bbbb")
    databaseHandler.getUserslist()
    return {"Request": "success"}


@app.get("/", response_class=HTMLResponse)
async def main_page() -> HTMLResponse:
    page = pages_dict.get("index.html")
    if page is None:
        raise FileNotFoundError("index.html not found!")
    else:
        return HTMLResponse(content=page, status_code=200)


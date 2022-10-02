import sys

sys.path.append("../../backend")

from core.database_handler import DatabaseHandler
from fastapi.responses import HTMLResponse
from core.sevice import upload_pages, base_logger
from fastapi import FastAPI
from core.endpoints.requests_models import *


def log(message: str) -> None:
    module_name = "ENDPOINTS"
    base_logger(msg=message, module_name=module_name)


sys.path.append("../../core")
pages_dict = upload_pages()
databaseHandler = DatabaseHandler()
app = FastAPI()


@app.post("/sign_up")
async def sign_up(signup_info: Signup_request) -> dict:
    log(f"REQUEST /sign_up: name = {signup_info.name}")
    success, response_msg = databaseHandler.signUp(signup_info.name, signup_info.password)
    log(f"RESPONSE /sign_up: success = {success}, response_msg = {response_msg}")
    return {"Success": success, "Response": response_msg}


@app.get("/", response_class=HTMLResponse)
async def main_page() -> HTMLResponse:
    page = pages_dict.get("index.html")
    if page is None:
        raise FileNotFoundError("index.html not found!")
    else:
        return HTMLResponse(content=page, status_code=200)

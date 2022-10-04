import sys

sys.path.append("../../backend")

from core.database_handler import DatabaseHandler
from fastapi.responses import HTMLResponse
from core.service import upload_pages, base_logger, update_main_page
from fastapi import FastAPI
from core.endpoints.requests_models import *
from core.auth_handler import Auth

def log(message: str) -> None:
    module_name = "ENDPOINTS"
    base_logger(msg=message, module_name=module_name)


sys.path.append("../../core")
pages_dict = upload_pages()
databaseHandler = DatabaseHandler()
app = FastAPI()
auth_handler = Auth(databaseHandler)

@app.post("/sign_up")
async def sign_up(signup_info: Signup_request) -> dict:
    log(f"REQUEST /sign_up: name = {signup_info.username}")
    success, response_msg = auth_handler.sign_up(signup_info.username, signup_info.password)
    log(f"RESPONSE /sign_up: success = {success}, response_msg = {response_msg}")
    return {"Success": success, "Response": response_msg}


@app.post("/login")
async def login(lodin_info: Login_request) -> None:
    pass


@app.get("/refresh_token")
async def refresh_token() -> None:
    pass


@app.get("/", response_class=HTMLResponse)
async def main_page() -> HTMLResponse:
    log("Main page request")
    page = pages_dict.get("index.html")
    product_col_rows = databaseHandler.get_product_cols()
    full_page = update_main_page(page, product_col_rows)
    if page is None:
        log("index.html not found!")
        raise FileNotFoundError("index.html not found!")
    else:
        log("HTMLResponse: index.html")
        return HTMLResponse(content=full_page, status_code=200)

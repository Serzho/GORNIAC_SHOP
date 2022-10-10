import sys

sys.path.append("../../backend")

from typing import Optional
from core.database_handler import DatabaseHandler
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from core.service import upload_pages, base_logger, update_main_page, update_signup_page
from fastapi import FastAPI, Depends, HTTPException, Header, Request
from core.endpoints.requests_models import *
from fastapi_jwt_auth import AuthJWT
from core.auth_handler import Auth


def log(message: str) -> None:
    module_name = "ENDPOINTS"
    base_logger(msg=message, module_name=module_name)


sys.path.append("../../core")
pages_dict = upload_pages()
databaseHandler = DatabaseHandler()
app = FastAPI()
auth_handler = Auth(databaseHandler)


@AuthJWT.load_config
def get_config():
    return Settings()


@app.get("/login", response_class=HTMLResponse)
async def login_page() -> HTMLResponse:
    return HTMLResponse(content=pages_dict["login.html"], status_code=200)


@app.get("/signup", response_class=HTMLResponse)
async def signup_page() -> HTMLResponse:
    return HTMLResponse(content=pages_dict["signup.html"], status_code=200)


@app.get("/signup/result={message}", response_class=HTMLResponse)
async def signup_page(message: str) -> HTMLResponse:
    page = pages_dict["signup.html"]
    page = update_signup_page(page, message)
    return HTMLResponse(content=page, status_code=200)


@app.post("/auth/login")
async def login(login_info: Login_form = Depends(Login_form.as_form), Authorize: AuthJWT = Depends()) -> HTTPException or dict:
    success, response_msg = auth_handler.login(login_info.username, login_info.password)
    print(success, response_msg)
    if not success:
        return HTTPException(status_code=401, detail=response_msg)
    else:
        access_token = Authorize.create_access_token(subject=login_info.username)
        refresh_token = Authorize.create_refresh_token(subject=login_info.username)
        Authorize.set_access_cookies(access_token)
        Authorize.set_refresh_cookies(refresh_token)
        return {"msg": "Successfully login"}


@app.get("/profile")
async def profile_page(Authorize: AuthJWT = Depends()) -> HTMLResponse or RedirectResponse:
    Authorize.jwt_required()

    current_user = Authorize.get_jwt_subject()
    print(current_user)
    return RedirectResponse("/login")


@app.post("/auth/signup")
async def signup(signup_info: Signup_form = Depends(Signup_form.as_form)) -> RedirectResponse or HTMLResponse:
    success, response_msg = auth_handler.sign_up(signup_info.username, signup_info.password)
    if success:
        return RedirectResponse("/login", status_code=303)
    else:
        return RedirectResponse(f"/signup/result={response_msg}", status_code=303)


@app.get("/refresh_token")
async def refresh_token(Authorize: AuthJWT = Depends()):
    Authorize.jwt_refresh_token_required()
    current_user = Authorize.get_jwt_subject()
    new_access_token = Authorize.create_access_token(subject=current_user)
    Authorize.set_access_cookies(new_access_token)
    return {"msg": "The token has been refresh"}


@app.delete('/auth/logout')
def logout(Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    Authorize.unset_jwt_cookies()
    return {"msg":"Successfully logout"}


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

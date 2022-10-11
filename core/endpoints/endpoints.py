import sys


from core.database_handler import DatabaseHandler
from fastapi.responses import HTMLResponse, RedirectResponse
from core.service import upload_pages, base_logger
from core.pages_loader import load_profile_page, load_main_page, load_signup_page
from fastapi import FastAPI, Depends, HTTPException
from core.endpoints.requests_models import *
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import MissingTokenError, JWTDecodeError
from core.auth_handler import Auth
from time import sleep


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
    page = load_signup_page(page, message)
    return HTMLResponse(content=page, status_code=200)


@app.post("/auth/login")
async def login(login_info: Login_form = Depends(Login_form.as_form), Authorize: AuthJWT = Depends()) -> HTTPException or HTMLResponse:
    success, response_msg = auth_handler.login(login_info.username, login_info.password)
    print(success, response_msg)
    if not success:
        return HTTPException(status_code=401, detail=response_msg)
    else:
        response = RedirectResponse(url="/", status_code=303)
        access_token = Authorize.create_access_token(subject=login_info.username)
        refreshed_token = Authorize.create_refresh_token(subject=login_info.username)
        Authorize.set_access_cookies(access_token, response=response)
        Authorize.set_refresh_cookies(refreshed_token, response=response)
        return response


@app.get("/profile")
async def profile_page(Authorize: AuthJWT = Depends()) -> HTMLResponse or RedirectResponse:
    try:
        Authorize.jwt_required()
        return HTMLResponse(content=load_profile_page(pages_dict["profile.html"]), status_code=200)
    except (MissingTokenError, JWTDecodeError):
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


@app.get('/auth/logout')
def logout(Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
        Authorize.unset_jwt_cookies()
        return {"msg": "Logout successfully response"}
    except (MissingTokenError, JWTDecodeError):
        return {"msg": "Logout exception!!!"}


@app.get("/", response_class=HTMLResponse)
async def main_page(Authorize: AuthJWT = Depends()) -> HTMLResponse:
    log("Main page request")
    page = pages_dict.get("index.html")
    product_col_rows = databaseHandler.get_product_cols()
    try:
        Authorize.jwt_required()
        username = Authorize.get_jwt_subject()
        is_authorized = True
    except (MissingTokenError, JWTDecodeError):
        is_authorized, username = False, None
    print(username)
    full_page = load_main_page(page, product_col_rows, is_authorized, username)
    if page is None:
        log("index.html not found!")
        raise FileNotFoundError("index.html not found!")
    else:
        log("HTMLResponse: index.html")
        return HTMLResponse(content=full_page, status_code=200)

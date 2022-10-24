from core.database_handler import DatabaseHandler
from fastapi.responses import HTMLResponse, RedirectResponse
from core.service import upload_pages, base_logger
from core.pages_loader import load_profile_page, load_main_page, load_signup_page, load_login_page, load_basket_page, add_authorized_effects
from fastapi import FastAPI, Depends
from core.endpoints.requests_models import *
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import MissingTokenError, JWTDecodeError
from core.auth_handler import Auth
from core.basket_handler import BasketHandler


pages_dict = upload_pages()
databaseHandler = DatabaseHandler()
app = FastAPI()
auth_handler = Auth(databaseHandler)
order_dict = {}
basket_handler = BasketHandler(databaseHandler)


def log(message: str) -> None:
    module_name = "ENDPOINTS"
    base_logger(msg=message, module_name=module_name)


@AuthJWT.load_config
def get_config() -> Settings:
    log("Loading AuthJWT config...")
    return Settings()


@app.get("/login", response_class=HTMLResponse)
async def login_page() -> HTMLResponse:
    log("Getting login page request")
    return HTMLResponse(content=pages_dict["login.html"], status_code=200)


@app.get("/login/result={message}", response_class=HTMLResponse)
async def login_page(message: str) -> HTMLResponse:
    log(f"Getting login page with message={message}")
    page = pages_dict["login.html"]
    page = load_login_page(page, message)
    return HTMLResponse(content=page, status_code=200)


@app.post("/order", response_class=RedirectResponse)
async def order(Authorize: AuthJWT = Depends()) -> RedirectResponse:
    log("Order request")
    try:
        Authorize.jwt_required()
        current_user = Authorize.get_jwt_subject()
        log(f"Order for user={current_user}")
    except (MissingTokenError, JWTDecodeError):
        log("User not authorized for order!")
        return RedirectResponse("/")
    success, response_msg = basket_handler.check_order(current_user)
    if success:
        log(f"Ordering for user {current_user}")
        basket_handler.order(current_user)


@app.get("/about", response_class=HTMLResponse)
async def about_page(Authorize: AuthJWT = Depends()) -> HTMLResponse:
    log("Getting about page request")
    page = pages_dict["about.html"]
    try:
        Authorize.jwt_required()
        current_user = Authorize.get_jwt_subject()
        log(f"Getting about page for user={current_user}")
        page = add_authorized_effects(page, current_user)
    except (MissingTokenError, JWTDecodeError):
        log("User not authorized!")
    return HTMLResponse(content=page, status_code=200)


@app.get("/news", response_class=HTMLResponse)
async def news_page(Authorize: AuthJWT = Depends()) -> HTMLResponse:
    log("Getting news page request")
    page = pages_dict["news.html"]
    try:
        Authorize.jwt_required()
        current_user = Authorize.get_jwt_subject()
        log(f"Getting news page for user={current_user}")
        page = add_authorized_effects(page, current_user)
    except (MissingTokenError, JWTDecodeError):
        log("User not authorized!")

    return HTMLResponse(content=page, status_code=200)


@app.get("/contacts", response_class=HTMLResponse)
async def contacts_page(Authorize: AuthJWT = Depends()) -> HTMLResponse:
    log("Getting contacts page request")
    page = pages_dict["contacts.html"]
    try:
        Authorize.jwt_required()
        current_user = Authorize.get_jwt_subject()
        log(f"Getting contacts page for user={current_user}")
        page = add_authorized_effects(page, current_user)
    except (MissingTokenError, JWTDecodeError):
        log("User not authorized!")

    return HTMLResponse(content=page, status_code=200)


@app.get("/signup", response_class=HTMLResponse)
async def signup_page() -> HTMLResponse:
    log("Getting signup page request")
    return HTMLResponse(content=pages_dict["signup.html"], status_code=200)


@app.get("/signup/result={message}", response_class=HTMLResponse)
async def signup_page(message: str) -> HTMLResponse:
    log(f"Getting signup page with message={message}")
    page = pages_dict["signup.html"]
    page = load_signup_page(page, message)
    return HTMLResponse(content=page, status_code=200)


@app.get("/add_to_basket/product={product_id}", response_class=RedirectResponse)
async def add_to_basket(product_id: str, Authorize: AuthJWT = Depends()) -> RedirectResponse:
    log(f"Adding product to basket request with product_id={product_id}")
    try:
        Authorize.jwt_required()
        current_user = Authorize.get_jwt_subject()
        log(f"Adding product for user={current_user}")
    except (MissingTokenError, JWTDecodeError):
        log("User not authorized! Redirecting to login page")
        return RedirectResponse("/login")
    basket_handler.add_product(current_user, int(product_id))
    log("Successfully added, redirecting to main page")
    return RedirectResponse(url="/", status_code=303)


@app.get("/increase_from_basket/product={product_name}", response_class=RedirectResponse)
async def increase_from_basket(product_name: str, Authorize: AuthJWT = Depends()) -> RedirectResponse:
    log(f"Increasing product from basket request with product_name={product_name}")
    try:
        Authorize.jwt_required()
        current_user = Authorize.get_jwt_subject()
        log(f"Increasing product for user={current_user}")
    except (MissingTokenError, JWTDecodeError):
        log("User not authorized! Redirecting to login page")
        return RedirectResponse("/login")
    product_id = databaseHandler.get_product_id(product_name)
    basket_handler.add_product(current_user, product_id)
    log("Successfully increased, redirecting to basket page")
    return RedirectResponse(url="/basket", status_code=303)


@app.get("/decrease_from_basket/product={product_name}", response_class=RedirectResponse)
async def decrease_from_basket(product_name: str, Authorize: AuthJWT = Depends()) -> RedirectResponse:
    log(f"Decreasing product from basket request with product_name={product_name}")
    try:
        Authorize.jwt_required()
        current_user = Authorize.get_jwt_subject()
        log(f"Decreasing product for user={current_user}")
    except (MissingTokenError, JWTDecodeError):
        log("User not authorized! Redirecting to login page")
        return RedirectResponse("/login")
    basket_handler.decrease_product(current_user, product_name)
    log("Successfully decreased, redirecting to basket page")
    return RedirectResponse(url="/basket", status_code=303)


@app.post("/auth/login", response_class=RedirectResponse)
async def login(login_info: LoginForm = Depends(LoginForm.as_form),
                Authorize: AuthJWT = Depends()) -> RedirectResponse:

    log(f"Login request: username={login_info.username}")
    success, response_msg = auth_handler.login(login_info.username, login_info.password)
    log(f"Login result: success={success}, response_msg={response_msg}")
    if not success:
        log("Redirecting to login page")
        return RedirectResponse(f"/login/result={response_msg}", status_code=303)
    else:
        log("Creating access and refresh tokens")
        response = RedirectResponse(url="/", status_code=303)
        access_token = Authorize.create_access_token(subject=login_info.username)
        refreshed_token = Authorize.create_refresh_token(subject=login_info.username)
        Authorize.set_access_cookies(access_token, response=response)
        Authorize.set_refresh_cookies(refreshed_token, response=response)
        log("Redirecting to main page with tokens")
        return response


@app.get("/profile")
async def profile_page(Authorize: AuthJWT = Depends()) -> HTMLResponse or RedirectResponse:
    log("Getting profile page request")
    try:
        Authorize.jwt_required()
        current_user = Authorize.get_jwt_subject()
        log(f"Returning profile page for user={current_user}")
        page = add_authorized_effects(pages_dict["profile.html"], current_user)
        return HTMLResponse(content=load_profile_page(page, current_user), status_code=200)
    except (MissingTokenError, JWTDecodeError):
        log("User not authorized! Redirecting to login page")
        return RedirectResponse("/login")


@app.post("/auth/signup", response_class=RedirectResponse)
async def signup(signup_info: SignupForm = Depends(SignupForm.as_form)) -> RedirectResponse:
    log(f"Signup request: name={signup_info.username}")
    success, response_msg = auth_handler.sign_up(signup_info.username, signup_info.password, signup_info.email)
    log(f"Signup request result: success={success}, response_msg={response_msg}")
    if success:
        log("Redirecting to login page")
        return RedirectResponse("/login", status_code=303)
    else:
        log("Redirecting to signup page ")
        return RedirectResponse(f"/signup/result={response_msg}", status_code=303)


@app.get("/refresh_token")
async def refresh_token(Authorize: AuthJWT = Depends()):
    log("Refreshing token request")
    Authorize.jwt_refresh_token_required()
    current_user = Authorize.get_jwt_subject()
    new_access_token = Authorize.create_access_token(subject=current_user)
    Authorize.set_access_cookies(new_access_token)
    return {}


@app.get('/auth/logout', response_class=RedirectResponse)
def logout(Authorize: AuthJWT = Depends()) -> RedirectResponse:
    log("Logout request")
    response = RedirectResponse(url="/", status_code=303)
    try:
        Authorize.jwt_required()
        Authorize.unset_jwt_cookies(response)
        log("JWT was deleted from cookie")
    except (MissingTokenError, JWTDecodeError):
        log("JWT was not found in cookie!")
    finally:
        return response


@app.get('/basket')
def basket_page(Authorize: AuthJWT = Depends()) -> RedirectResponse or HTMLResponse:
    log("Basket page request")
    try:
        Authorize.jwt_required()
        username = Authorize.get_jwt_subject()
        log(f"Basket page request from authorized user: username={username}")
        page = add_authorized_effects(pages_dict["basket.html"], username)
    except (MissingTokenError, JWTDecodeError):
        log(f"Basket page request from non-authorized user")
        log("Redirecting to login page")
        return RedirectResponse("/login", status_code=303)

    basket_dict = basket_handler.get_basket_list(username)
    page = load_basket_page(page, username, basket_dict)
    log("Returning up-to-date basket page")
    return HTMLResponse(content=page, status_code=200)


@app.get("/", response_class=HTMLResponse)
async def main_page(Authorize: AuthJWT = Depends()) -> HTMLResponse:
    log("Main page request")
    page = pages_dict.get("index.html")
    product_col_rows = databaseHandler.get_product_cols()
    try:
        Authorize.jwt_required()
        username = Authorize.get_jwt_subject()
        is_authorized = True
        log(f"Main page request from authorized user: username={username}")
        page = add_authorized_effects(page, username)
    except (MissingTokenError, JWTDecodeError):
        is_authorized, username = False, None
        log(f"Main page request from non-authorized user")
    full_page = load_main_page(page, product_col_rows, is_authorized)
    if page is None:
        log("index.html not found!")
        raise FileNotFoundError("index.html not found!")
    else:
        log("HTMLResponse: index.html")
        return HTMLResponse(content=full_page, status_code=200)

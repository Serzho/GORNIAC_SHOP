import time
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi import FastAPI, Depends
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import MissingTokenError, JWTDecodeError
from core.database_handler import DatabaseHandler
from core.service import upload_pages, base_logger
from core.pages_loader import load_profile_page, load_main_page, load_signup_page, load_login_page, load_basket_page, \
    add_authorized_effects, load_admin_panel_page
from core.endpoints.requests_models import *
from core.auth_handler import Auth
from core.basket_handler import BasketHandler
from core.email_handler import EmailHandler


pages_dict = upload_pages()
database_handler = DatabaseHandler()
app = FastAPI()
email_handler = EmailHandler()
auth_handler = Auth(database_handler, email_handler)
order_dict = {}

basket_handler = BasketHandler(database_handler, email_handler)


def log(message: str) -> None:
    module_name = "ENDPOINTS"
    base_logger(msg=message, module_name=module_name)


@AuthJWT.load_config
def get_config() -> Settings:
    log("Loading AuthJWT config...")
    return Settings()


@app.post("/admin_panel/adding_product", response_class=RedirectResponse)
async def adding_product(
        product_info: AdminAddingProductForm = Depends(AdminAddingProductForm.as_form),
        authorize: AuthJWT = Depends()) -> RedirectResponse:
    log(f"Adding product from admin panel request: product={product_info}")
    try:
        authorize.jwt_required()
        current_user = authorize.get_jwt_subject()
        assert current_user == "admin"
        log("Admin was authenticated")
    except (MissingTokenError, JWTDecodeError, AssertionError):
        log("Authenticated error!")
        return RedirectResponse("/login")
    log("Adding product to database")
    database_handler.add_product(
        nicotine=product_info.nicotine,
        vp_pg=product_info.vp_pg,
        product_name=product_info.name,
        description=product_info.description,
        logo_file=product_info.logo_file,
        price=product_info.price,
        volume=product_info.volume,
        rating=product_info.rating
    )
    return RedirectResponse("/admin_panel/", status_code=303)


@app.post("/admin_panel/adding_item", response_class=RedirectResponse)
async def adding_item(
        item_info: AdminAddingItemForm = Depends(AdminAddingItemForm.as_form),
        authorize: AuthJWT = Depends()) -> RedirectResponse:
    log(f"Adding item from admin panel request: item_info={item_info}")
    try:
        authorize.jwt_required()
        current_user = authorize.get_jwt_subject()
        assert current_user == "admin"
        log("Admin was authenticated")
    except (MissingTokenError, JWTDecodeError, AssertionError):
        log("Authenticated error!")
        return RedirectResponse("/login")
    log("Adding item to database")
    database_handler.add_items(item_info.product_id, item_info.count)
    return RedirectResponse("/admin_panel/", status_code=303)


@app.post("/admin_panel/refresh_amounts", response_class=RedirectResponse)
async def refresh_amounts(authorize: AuthJWT = Depends()) -> RedirectResponse:
    log("Refreshing amount from admin panel request")
    try:
        authorize.jwt_required()
        current_user = authorize.get_jwt_subject()
        assert current_user == "admin"
        log("Admin was authenticated")
    except (MissingTokenError, JWTDecodeError, AssertionError):
        log("Authenticated error!")
        return RedirectResponse("/login")
    log("Refreshing all amounts")
    database_handler.refresh_amounts()
    return RedirectResponse("/admin_panel/", status_code=303)


@app.post("/admin_panel/adding_promo", response_class=RedirectResponse)
async def adding_promo(
        promo_info: AdminAddingPromoForm = Depends(AdminAddingPromoForm.as_form),
        authorize: AuthJWT = Depends()) -> RedirectResponse:
    log(f"Adding promo from admin panel request: promo_info={promo_info}")
    try:
        authorize.jwt_required()
        current_user = authorize.get_jwt_subject()
        assert current_user == "admin"
        log("Admin was authenticated")
    except (MissingTokenError, JWTDecodeError, AssertionError):
        log("Authenticated error!")
        return RedirectResponse("/login")
    log("Adding promo")
    basket_handler.create_promocode(promo_info.user_id, promo_info.sale)
    return RedirectResponse("/admin_panel/", status_code=303)


@app.post("/admin_panel/delete_product", response_class=RedirectResponse)
async def delete_product(
        product_info: AdminDeletingProductForm = Depends(AdminDeletingProductForm.as_form),
        authorize: AuthJWT = Depends()) -> RedirectResponse:
    log(f"Deleting product from admin panel request: product_info={product_info}")
    try:
        authorize.jwt_required()
        current_user = authorize.get_jwt_subject()
        assert current_user == "admin"
        log("Admin was authenticated")
    except (MissingTokenError, JWTDecodeError, AssertionError):
        log("Authenticated error!")
        return RedirectResponse("/login")
    log("Deleting product")
    database_handler.delete_product(product_info.product_id)
    return RedirectResponse("/admin_panel/", status_code=303)


@app.post("/admin_panel/ban_user")
async def ban_user(
        ban_info: AdminBanUserForm = Depends(AdminBanUserForm.as_form),
        authorize: AuthJWT = Depends()) -> RedirectResponse:
    log(f"Ban user from admin panel request: ban_info={ban_info}")
    try:
        authorize.jwt_required()
        current_user = authorize.get_jwt_subject()
        assert current_user == "admin"
        log("Admin was authenticated")
    except (MissingTokenError, JWTDecodeError, AssertionError):
        log("Authenticated error!")
        return RedirectResponse("/login")
    log("Ban user")
    auth_handler.ban_user(ban_info.user_id, ban_info.ban_description)
    return RedirectResponse("/admin_panel/", status_code=303)


@app.get("/login", response_class=HTMLResponse)
async def login_page() -> HTMLResponse:
    log("Getting login page request")
    return HTMLResponse(content=load_login_page(pages_dict["login.html"]), status_code=200)


@app.get("/login{message}", response_class=HTMLResponse)
async def login_page(message: str) -> HTMLResponse:
    log(f"Getting login page with message={message}")
    page = pages_dict["login.html"]
    page = load_login_page(page, message)
    return HTMLResponse(content=page, status_code=200)


@app.get("/good_order", response_class=HTMLResponse)
async def good_order_page() -> HTMLResponse:
    log(f"Getting good order page")
    page = pages_dict["order.html"]
    return HTMLResponse(content=page, status_code=200)


@app.post("/order", response_class=RedirectResponse)
async def order(order_info: OrderForm = Depends(OrderForm.as_form),
                authorize: AuthJWT = Depends()) -> RedirectResponse:
    log("Order request")
    try:
        authorize.jwt_required()
        current_user = authorize.get_jwt_subject()
        log(f"Order for user={current_user}")
    except (MissingTokenError, JWTDecodeError):
        log("User not authorized for order!")
        return RedirectResponse("/login")
    success, response_msg = basket_handler.check_order(current_user, order_info.promocode)
    if success:
        log(f"Ordering for user {current_user}")
        basket_handler.order(current_user, order_info.promocode)
        return RedirectResponse(url="/good_order", status_code=303)
    else:
        log(f"Order failed: {response_msg}")
        return RedirectResponse(url=f"/basket{response_msg}", status_code=303)


@app.get("/about", response_class=HTMLResponse)
async def about_page(authorize: AuthJWT = Depends()) -> HTMLResponse:
    log("Getting about page request")
    page = pages_dict["about.html"]
    try:
        authorize.jwt_required()
        current_user = authorize.get_jwt_subject()
        log(f"Getting about page for user={current_user}")
        page = add_authorized_effects(page, current_user)
    except (MissingTokenError, JWTDecodeError):
        log("User not authorized!")
    return HTMLResponse(content=page, status_code=200)


@app.get("/news", response_class=HTMLResponse)
async def news_page(authorize: AuthJWT = Depends()) -> HTMLResponse:
    log("Getting news page request")
    page = pages_dict["news.html"]
    try:
        authorize.jwt_required()
        current_user = authorize.get_jwt_subject()
        log(f"Getting news page for user={current_user}")
        page = add_authorized_effects(page, current_user)
    except (MissingTokenError, JWTDecodeError):
        log("User not authorized!")

    return HTMLResponse(content=page, status_code=200)


@app.post("/admin_panel/complete_order{order_name}", response_class=RedirectResponse)
async def complete_order(
        order_name: str,
        authorize: AuthJWT = Depends()) -> RedirectResponse:
    log(f"Complete order from admin panel request: order_name={order_name}")
    try:
        authorize.jwt_required()
        current_user = authorize.get_jwt_subject()
        assert current_user == "admin"
        log("Admin was authenticated")
    except (MissingTokenError, JWTDecodeError, AssertionError):
        log("Authenticated error!")
        return RedirectResponse("/login")
    log("Completing order")
    database_handler.complete_order(order_name.replace('.', "#"))
    return RedirectResponse("/admin_panel/", status_code=303)


@app.post("/cancel_order{order_name}")
async def cancel_order(
        order_name: str,
        authorize: AuthJWT = Depends()) -> RedirectResponse:
    log(f"Canceling order request: order_name={order_name}")
    try:
        authorize.jwt_required()
        current_user = authorize.get_jwt_subject()
        order_name = order_name.replace('.', "#")
        username_from_order = database_handler.get_user_info_from_order(order_name)["username"]
        assert current_user == "admin" or current_user == username_from_order
        log("Admin or current user authenticated")
    except (MissingTokenError, JWTDecodeError, AssertionError):
        log("Authenticated error!")
        return RedirectResponse("/login")
    log("Canceling order")
    database_handler.cancel_order(order_name)
    if current_user == "admin":
        return RedirectResponse("/admin_panel", status_code=303)
    else:
        return RedirectResponse("/", status_code=303)


@app.get("/admin_panel")
async def admin_panel_page(authorize: AuthJWT = Depends()) -> HTMLResponse or RedirectResponse:
    log("Getting admin panel page request")
    page = pages_dict["admin_panel.html"]
    try:
        authorize.jwt_required()
        current_user = authorize.get_jwt_subject()
        if current_user == "admin":
            log("User is admin, getting admin panel")
            page = add_authorized_effects(page, current_user)
            incompleted_orders = basket_handler.get_incompleted_orders_list()
            users = database_handler.get_all_users()
            products = database_handler.get_all_products()
            page = load_admin_panel_page(page, incompleted_orders, users, products)
            return HTMLResponse(content=page, status_code=200)
    except (MissingTokenError, JWTDecodeError):
        log("Admin panel request from non-authorized user!")
    log("User is not admin!")
    return RedirectResponse(url="/login", status_code=303)


@app.get("/contacts", response_class=HTMLResponse)
async def contacts_page(authorize: AuthJWT = Depends()) -> HTMLResponse:
    log("Getting contacts page request")
    page = pages_dict["contacts.html"]
    try:
        authorize.jwt_required()
        current_user = authorize.get_jwt_subject()
        log(f"Getting contacts page for user={current_user}")
        page = add_authorized_effects(page, current_user)
    except (MissingTokenError, JWTDecodeError):
        log("User not authorized!")

    return HTMLResponse(content=page, status_code=200)


@app.get("/signup", response_class=HTMLResponse)
async def signup_page() -> HTMLResponse:
    log("Getting signup page request")
    return HTMLResponse(content=load_signup_page(pages_dict["signup.html"]), status_code=200)


@app.get("/ban", response_class=HTMLResponse)
async def ban_page() -> HTMLResponse:
    log("Getting ban page request")
    return HTMLResponse(content=pages_dict["ban_page.html"], status_code=200)


@app.get("/signup{message}", response_class=HTMLResponse)
async def signup_page(message: str) -> HTMLResponse:
    log(f"Getting signup page with message={message}")
    page = pages_dict["signup.html"]
    page = load_signup_page(page, message)
    return HTMLResponse(content=page, status_code=200)


@app.get("/add_to_basket/product={product_id}", response_class=RedirectResponse)
async def add_to_basket(product_id: str, authorize: AuthJWT = Depends()) -> RedirectResponse:
    log(f"Adding product to basket request with product_id={product_id}")
    try:
        authorize.jwt_required()
        current_user = authorize.get_jwt_subject()
        log(f"Adding product for user={current_user}")
    except (MissingTokenError, JWTDecodeError):
        log("User not authorized! Redirecting to login page")
        return RedirectResponse("/login")
    basket_handler.add_product(current_user, int(product_id))
    log("Successfully added, redirecting to main page")
    return RedirectResponse(url="/", status_code=303)


@app.get("/test")  # TODO: REMOVE FOR RELEASE
async def test_func():
    print(basket_handler.get_orders_list("admin"))


@app.get("/increase_from_basket/product={product_name}", response_class=RedirectResponse)
async def increase_from_basket(product_name: str, authorize: AuthJWT = Depends()) -> RedirectResponse:
    log(f"Increasing product from basket request with product_name={product_name}")
    try:
        authorize.jwt_required()
        current_user = authorize.get_jwt_subject()
        log(f"Increasing product for user={current_user}")
    except (MissingTokenError, JWTDecodeError):
        log("User not authorized! Redirecting to login page")
        return RedirectResponse("/login")
    product_id = database_handler.get_product_id(product_name)
    basket_handler.add_product(current_user, product_id)
    log("Successfully increased, redirecting to basket page")
    return RedirectResponse(url="/basket", status_code=303)


@app.get("/decrease_from_basket/product={product_name}", response_class=RedirectResponse)
async def decrease_from_basket(product_name: str, authorize: AuthJWT = Depends()) -> RedirectResponse:
    log(f"Decreasing product from basket request with product_name={product_name}")
    try:
        authorize.jwt_required()
        current_user = authorize.get_jwt_subject()
        log(f"Decreasing product for user={current_user}")
    except (MissingTokenError, JWTDecodeError):
        log("User not authorized! Redirecting to login page")
        return RedirectResponse("/login")
    basket_handler.decrease_product(current_user, product_name)
    log("Successfully decreased, redirecting to basket page")
    return RedirectResponse(url="/basket", status_code=303)


@app.post("/auth/login", response_class=RedirectResponse)
async def login(login_info: LoginForm = Depends(LoginForm.as_form),
                authorize: AuthJWT = Depends()) -> RedirectResponse:
    log(f"Login request: username={login_info.username}")
    if login_info.username != "empty" and login_info.password != "empty":
        success, response_msg = auth_handler.login(login_info.username, login_info.password)
    else:
        success, response_msg = False, "Username or password is empty!"
    log(f"Login result: success={success}, response_msg={response_msg}")
    if not success:
        if response_msg == "BAN":
            return RedirectResponse("/ban", status_code=303)
        log("Redirecting to login page")
        return RedirectResponse(f"/login{response_msg}", status_code=303)
    else:
        log("Creating access and refresh tokens")
        response = RedirectResponse(url="/", status_code=303)
        access_token = authorize.create_access_token(subject=login_info.username)
        refreshed_token = authorize.create_refresh_token(subject=login_info.username)
        authorize.set_access_cookies(access_token, response=response)
        authorize.set_refresh_cookies(refreshed_token, response=response)
        log("Redirecting to main page with tokens")
        return response


@app.get("/profile")
async def profile_page(authorize: AuthJWT = Depends()) -> HTMLResponse or RedirectResponse:
    log("Getting profile page request")
    try:
        authorize.jwt_required()
        current_user = authorize.get_jwt_subject()
        log(f"Returning profile page for user={current_user}")
        page = add_authorized_effects(pages_dict["profile.html"], current_user)
        orders_list = basket_handler.get_orders_list(current_user)
        return HTMLResponse(
            content=load_profile_page(
                page, current_user, database_handler.get_user_email(current_user), None, orders_list
            ),
            status_code=200
        )
    except (MissingTokenError, JWTDecodeError):
        log("User not authorized! Redirecting to login page")
        return RedirectResponse("/login")


@app.get("/profile{message}")
async def profile_page(message: str, authorize: AuthJWT = Depends()) -> HTMLResponse or RedirectResponse:
    log(f"Getting profile page request with message={message}")
    try:
        authorize.jwt_required()
        current_user = authorize.get_jwt_subject()
        log(f"Returning profile page for user={current_user}")
        page = add_authorized_effects(pages_dict["profile.html"], current_user)
        orders_list = basket_handler.get_orders_list(current_user)
        return HTMLResponse(
            content=load_profile_page(
                page, current_user, database_handler.get_user_email(current_user), message, orders_list
            ),
            status_code=200
        )
    except (MissingTokenError, JWTDecodeError):
        log("User not authorized! Redirecting to login page")
        return RedirectResponse("/login")


@app.post("/auth/signup", response_class=RedirectResponse)
async def signup(signup_info: SignupForm = Depends(SignupForm.as_form)) -> RedirectResponse:
    log(f"Signup request: name={signup_info.username}")
    if signup_info.password != "empty" and signup_info.username != "empty" and signup_info.email != "empty":
        success, response_msg = auth_handler.sign_up(signup_info.username, signup_info.password, signup_info.email)
    else:
        success, response_msg = False, "Empty field!"
    log(f"Signup request result: success={success}, response_msg={response_msg}")
    if success:
        basket_handler.create_promocode(database_handler.get_user_id(signup_info.username), 50)
        log("Redirecting to login page")
        return RedirectResponse("/login", status_code=303)
    else:
        log("Redirecting to signup page ")
        return RedirectResponse(f"/signup{response_msg}", status_code=303)


@app.post("/auth/change_password", response_class=RedirectResponse)
async def change_password(
        update_info: ChangePasswordForm = Depends(ChangePasswordForm.as_form),
        authorize: AuthJWT = Depends()) -> RedirectResponse:
    log("Changing password request")
    try:
        authorize.jwt_required()
        username = authorize.get_jwt_subject()
        log(f"Changing password for user={username}")
    except (MissingTokenError, JWTDecodeError):
        log("User not authorized!")
        return RedirectResponse("/login", status_code=303)
    if update_info.password != "empty":
        success, response_msg = auth_handler.change_password(username, update_info.password)
    else:
        success, response_msg = False, "Password is empty!"
    log(f"Changing password: success={success}, response={response_msg}")
    return RedirectResponse(f"/profile{response_msg}", status_code=303)


@app.post("/auth/change_email", response_class=RedirectResponse)
async def change_email(
        update_info: ChangeEmailForm = Depends(ChangeEmailForm.as_form),
        authorize: AuthJWT = Depends()) -> RedirectResponse:
    log("Changing email request")
    try:
        authorize.jwt_required()
        username = authorize.get_jwt_subject()
        log(f"Changing email for user={username}")
    except (MissingTokenError, JWTDecodeError):
        log("User not authorized!")
        return RedirectResponse("/login", status_code=303)
    if update_info.email != "empty":
        success, response_msg = auth_handler.change_email(username, update_info.email)
    else:
        success, response_msg = False, "Empty email!"
    log(f"Changing email: success={success}, response_msg={response_msg}")
    return RedirectResponse(f"/profile{response_msg}", status_code=303)


@app.get("/refresh_token")
async def refresh_token(authorize: AuthJWT = Depends()):
    log("Refreshing token request")
    authorize.jwt_refresh_token_required()
    current_user = authorize.get_jwt_subject()
    new_access_token = authorize.create_access_token(subject=current_user)
    authorize.set_access_cookies(new_access_token)
    return {}


@app.get('/auth/logout', response_class=RedirectResponse)
def logout(authorize: AuthJWT = Depends()) -> RedirectResponse:
    log("Logout request")
    response = RedirectResponse(url="/", status_code=303)
    try:
        authorize.jwt_required()
        authorize.unset_jwt_cookies(response)
        log("JWT was deleted from cookie")
    except (MissingTokenError, JWTDecodeError):
        log("JWT was not found in cookie!")
    finally:
        return response


@app.get('/basket')
def basket_page(authorize: AuthJWT = Depends()) -> RedirectResponse or HTMLResponse:
    log("Basket page request")
    try:
        authorize.jwt_required()
        username = authorize.get_jwt_subject()
        log(f"Basket page request from authorized user: username={username}")
        page = add_authorized_effects(pages_dict["basket.html"], username)
    except (MissingTokenError, JWTDecodeError):
        log(f"Basket page request from non-authorized user")
        log("Redirecting to login page")
        return RedirectResponse("/login", status_code=303)

    basket_dict = basket_handler.get_basket_list(username)
    promo = database_handler.get_user_promo(username)
    page = load_basket_page(page, username, basket_dict, None, promo)
    log("Returning up-to-date basket page")
    return HTMLResponse(content=page, status_code=200)


@app.get('/basket{message}')
def basket_page(message: str, authorize: AuthJWT = Depends()) -> RedirectResponse or HTMLResponse:
    log("Basket page request")
    try:
        authorize.jwt_required()
        username = authorize.get_jwt_subject()
        log(f"Basket page request from authorized user: username={username}")
        page = add_authorized_effects(pages_dict["basket.html"], username)
    except (MissingTokenError, JWTDecodeError):
        log(f"Basket page request from non-authorized user")
        log("Redirecting to login page")
        return RedirectResponse("/login", status_code=303)

    basket_dict = basket_handler.get_basket_list(username)
    promo = database_handler.get_user_promo(username)
    page = load_basket_page(page, username, basket_dict, message, promo)
    log("Returning up-to-date basket page")
    return HTMLResponse(content=page, status_code=200)


@app.get("/", response_class=HTMLResponse)
async def main_page(authorize: AuthJWT = Depends()) -> HTMLResponse:
    log("Main page request")
    page = pages_dict.get("index.html")
    product_col_rows = database_handler.get_product_cols()
    try:
        authorize.jwt_required()
        username = authorize.get_jwt_subject()
        is_authorized = True
        log(f"Main page request from authorized user: username={username}")
        page = add_authorized_effects(page, username)
    except (MissingTokenError, JWTDecodeError):
        is_authorized, username = False, None
        log(f"Main page request from non-authorized user")
    full_page = load_main_page(
        page,
        product_col_rows,
        is_authorized,
    )
    if page is None:
        log("index.html not found!")
        raise FileNotFoundError("index.html not found!")
    else:
        log("HTMLResponse: index.html")
        return HTMLResponse(content=full_page, status_code=200)


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    # print(f"Process time {process_time}")
    response.headers["X-Process-Time"] = str(process_time)
    return response

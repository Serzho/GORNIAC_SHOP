from jinja2 import Template
from core.service import base_logger


def log(message: str) -> None:
    base_logger(msg=message, module_name="PAGES_LOADER")


def load_profile_page(profile_html: str, username: str, email: str, message: str or None,
                      orders: list[dict] or None) -> str:
    log(f"Loading profile page: user={username}, email={email}, message={message} and {len(orders)} orders")
    profile_html = Template(profile_html).render({
        "message": message, "username": username, "email": email, "orders": orders
    })
    return profile_html


def load_admin_panel_page(
        panel_html: str, orders: list[dict] or None, users: list[dict], products: list[dict] or None) -> str:
    panel_html = Template(panel_html).render({
        'users': users, 'products': products, 'orders': orders
    })
    return panel_html


def load_signup_page(signup_html: str, message: str = None) -> str:
    log(f"Loading signup page with message={message}")
    return Template(signup_html).render({"message": message})


def load_login_page(login_html: str, message: str = None) -> str:
    log(f"Loading login page with message={message}")
    return Template(login_html).render({"message": message})


def add_authorized_effects(page_html: str, username: str) -> str:
    log(f"Adding authorized effects to page for user={username}")
    page_html = page_html.replace(
        '<div class="header__icons">',
        f'<div class="header__icons"><a href="auth/logout" class="header__link"><img src="static/images/logout.png" '
        f'alt="" height="41px" width="41px"> </a> '
    )
    page_html = page_html.replace(
        '</nav>',
        f'</nav>{username}'
    )
    return page_html


def load_basket_page(
        basket_html: str, name: str, basket_list: dict, message: str or None, promocodes: dict or None
) -> str:
    log(f"Updating basket page for user with name={name} with message={message}")
    basket_html = Template(basket_html).render({
        'promocodes': promocodes,
        'total': basket_list.get("total"),
        'products':  basket_list.get("products"),
        'message': message,
        'name': name
    })
    log("Returning up-to-date basket page")
    return basket_html


def load_main_page(index_html: str, products: list[dict], is_authorized: bool = False) -> str:
    log(f"Updating main page with {len(products)} products")
    index_html = Template(index_html).render({
        'products': products,
        'is_authorized': is_authorized
    })

    log("Returning up-to-date main page")
    return index_html

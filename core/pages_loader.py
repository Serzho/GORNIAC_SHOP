from jinja2 import Template
from service import base_logger


def log(message: str) -> None:
    base_logger(msg=message, module_name="PAGESLOADER")


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


def load_main_page(
        index_html: str, products: list[dict], is_authorized: bool = False, product_template: str = None, modal_template: str = None) -> str:
    log(f"Updating main page with {len(products)} products")
    product_cols = []
    modals = []

    for row in products:
        product_col = product_template
        modal = modal_template
        path = row["logo_file"]

        if row["is_demo"]:
            path = "static/images/logo/comingsoon.png"
            product_col = product_col.replace(
                'data-modal=',
                f''
            )
        elif row["amount_items"] == 0:
            path = path.replace("logo/", "logo/soldout/soldout_")
            product_col = product_col.replace(
                'data-modal=',
                f''
            )
        else:
            modal = modal.replace(
                '<div class="modal" id="">',
                f'<div class="modal" id="modal_product_{row["product_id"]}">'
            )

            modal = modal.replace(
                '<div class="modal__dialog ">',
                f'<div class="modal__dialog modal__dialog_product_{row["product_id"]}">'
            )

            modal = modal.replace(
                '<img class="modal-work__photo" src="">',
                f'<img class="modal-work__photo" src="{row["logo_file"]}" alt="#" '
                f'onerror="this.src = \'static/images/logo/alt_logo.png\'">'
            )

            modal = modal.replace(
                '<h3 class="modal-work__title">',
                f'<h3 class="modal-work__title">{row["product_name"]}'
            )

            modal = modal.replace(
                '</span>',
                f'</span>{row["amount_items"]} шт'
            )

            modal = modal.replace(
                '<div class="modal-work__about-chars-vgpg">',
                f'<div class="modal-work__about-chars-vgpg">VG/PG: {row["vg_pg"]}'
            )
            modal = modal.replace(
                '<div class="modal-work__about-chars-nic">',
                f'<div class="modal-work__about-chars-nic">NIC: {row["nicotine"]} mg/ml'
            )
            modal = modal.replace(
                '<div class="modal-work__about-chars-volume">',
                f'<div class="modal-work__about-chars-volume">{row["volume"]} ml'
            )

            modal = modal.replace(
                '<div class="modal-work__text">',
                f'<div class="modal-work__text">{row["description"]}'
            )

            modal = modal.replace(
                '<a href="#" class="btn  btn__buy">',
                f'<a href="/add_to_basket/product={row["product_id"]}" class="btn  btn__buy">'
            )
            product_col = product_col.replace(
                'data-modal=',
                f'data-modal=#modal_product_{row["product_id"]}'
            )

        product_col = product_col.replace(
            'class="product__image" src=',
            f'class="product__image" src="{path}" alt="" onerror="this.src = \'static/images/logo/alt_logo.png\'"'
        )
        product_col = product_col.replace(
            '<div class="product__name">',
            f'<div class="product__name">{row["product_name"]}'
        )
        product_col = product_col.replace(
            '<div class="product__date">',
            f'<div class="product__date">{row["dev_date"]}'
        )

        product_cols.append(product_col)
        modals.append(modal)

    modal_windows = " ".join(modals)
    catalog = " ".join(product_cols)

    index_html = index_html.replace(
        '<div class="catalog">',
        f'<div class="catalog">{catalog}'
    )

    index_html = index_html.replace(
        '<script src="static/js/app.js"></script>',
        f'{modal_windows}<script src="static/js/app.js"></script>'
    )

    if not is_authorized:
        index_html = index_html.replace(
            'class="btn  btn__buy">в корзину',
            'class="btn  btn__buy">авторизуйтесь'
        )

    log("Returning up-to-date main page")
    return index_html

from service import base_logger


def log(message: str) -> None:
    base_logger(msg=message, module_name="PAGESLOADER")


def load_profile_page(profile_html: str, username: str) -> str:
    log(f"Loading profile page for username {username}")
    # TODO: loading profile page
    return profile_html


def load_signup_page(signup_html: str, message: str) -> str:
    log(f"Loading signup page with message={message}")
    signup_html = signup_html.replace(
        '<body>',
        f'<body> <p><font size="5" color="red" face="Arial">{message}</font></p>'
    )
    return signup_html


def load_login_page(login_html: str, message: str) -> str:
    log(f"Loading login page with message={message}")
    login_html = login_html.replace(
        '<body>',
        f'<body> <p><font size="5" color="red" face="Arial">{message}</font></p>'
    )
    return login_html


def add_authorized_effects(page_html: str, username: str) -> str:
    page_html = page_html.replace(
        '<div class="header__icons">',
        f'<div class="header__icons"><a href="auth/logout"><img src="static/images/logout.png" alt="" height="41px" width="41px"> </a> '
    )
    page_html = page_html.replace(
        '</nav>',
        f'</nav>{username}'
    )
    return page_html


def load_basket_page(basket_html: str, name: str, basket_list: dict) -> str:
    log(f"Updating basket page for user with name={name}")
    total = basket_list.get("total")
    products = basket_list.get("products")
    basket_html = basket_html.replace('</body>', f'<h3>{name}</h3></body>')
    for product_name, price_and_amount in products.items():
        price = price_and_amount["price"]
        amount = price_and_amount["amount"]
        basket_html = basket_html.replace('</body>', f'<p>{product_name}, {price}, {amount} </p> '
                                                     f'<a href="/decrease_from_basket/product={product_name}"'
                                                     f' class="basket__link">'
                                                     f'<img src="static/images/minus.png" alt="" '
                                                     f'height="25px" width="25px"></a> '
                                                     f'<a href="/increase_from_basket/product={product_name}" '
                                                     f'class="basket__link">'
                                                     f'<img src="static/images/plus.png" alt="" '
                                                     f'height="25px" width="25px"></a></body>')
    basket_html = basket_html.replace('</body>', f'<p>{total}</p></body>')
    log("Returning up-to-date basket page")
    return basket_html


def load_main_page(index_html: str, products: list[dict], is_authorized: bool = False) -> str:
    log(f"Updating main page with {len(products)} products")
    product_cols = []
    modals = []

    template_file = open("templates/product_template.html", "r")
    product_template = template_file.read()
    template_file.close()

    template_file = open("templates/modal_product_template.html", "r", encoding="UTF-8")
    modal_template = template_file.read()
    template_file.close()

    for row in products:
        product_col = product_template
        modal = modal_template
        path = row["logo_file"]

        if not row["is_active"] and not row["is_demo"]:
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
                '<img class="modal-work__photo" src="" alt="#">',
                f'<img class="modal-work__photo" src="{row["logo_file"]}" alt="#">'
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
            f'class="product__image" src="{path}"'
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

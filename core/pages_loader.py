from service import base_logger


def log(message: str) -> None:
    base_logger(msg=message, module_name="PAGESLOADER")


def load_profile_page(profile_html: str, username: str, email: str, message: str or None,
                      orders: list[dict] or None) -> str:
    log(f"Loading profile page: user={username}, email={email}, message={message} and {len(orders)} orders")
    profile_html = profile_html.replace("<p><strong>Имя:</strong>", f"<p><strong>Имя:</strong> {username}")
    profile_html = profile_html.replace('placeholder=""', f'placeholder="{email}"')
    if message is not None:
        profile_html = profile_html.replace('<div class="profile__form">',
                                            f'<div class="profile__form"><p class="warning">{message}</p>')
    for order in orders[::-1]:
        product_table = ''
        for index, product in order["products"].items():
            product_table += f"<p>{product['product_name']} {product['amount']} шт.: {product['total']}</p>"
        completed = "да" if order["is_completed"] else "нет"
        cancel_button = f'<p><form action="/cancel_order{order["name"].replace("#", ".")}"' \
                        ' method="post"><input type="submit" ' \
                        'value="ОТМЕНИТЬ"/></form></p>' if not order['is_completed'] else ''
        profile_html = profile_html.replace(
            '<div class="orders">',
            f'<div class="orders">'
            f'<div class="order__col">Заказ {order["name"]} от {order["date"]}:'
            f' {product_table} <p> ИТОГО: {order["total_price"]}</p><p>Выполнен: {completed}</p>'
            f'{cancel_button}</div>'
        )

    return profile_html


def load_admin_panel_page(
        panel_html: str, orders: list[dict] or None, users: list[dict], products: list[dict] or None) -> str:
    for order in orders[::-1]:
        product_table = ''
        for index, product in order["products"].items():
            product_table += f"<p>{product['product_name']} {product['amount']} шт.: {product['total']}</p>"
        panel_html = panel_html.replace(
            '<h2> РАБОТА С ЗАКАЗАМИ </h2>',
            f'<h2> РАБОТА С ЗАКАЗАМИ </h2>'
            f'Заказ {order["name"]} от {order["date"]} для {order["username"]}, id {order["user_id"]}:'
            f' {product_table} <p> ИТОГО: {order["total_price"]}</p>'
            f'<p><form action="/admin_panel/complete_order{order["name"].replace("#", ".")}" method="post">'
            f'<input type="submit" value="ВЫПОЛНИТЬ"/></form></p>'
            f'<p><form action="/cancel_order{order["name"].replace("#", ".")}" method="post">'
            f'<input type="submit" value="ОТМЕНИТЬ"/></form></p>')
    for user in users:
        panel_html = panel_html.replace('<p>Пользователи</p><div class="dropdown_block"><ul>',
                                        f'<p>Пользователи</p><div class="dropdown_block"><ul>'
                                        f'<li>{user["name"]}, id={user["id"]}, бан={user["is_banned"]}</li>')
    if products is not None:
        for product in products:
            panel_html = panel_html.replace('<p>Продукты</p><div class="dropdown_block"><ul>',
                                            '<p>Продукты</p><div class="dropdown_block"><ul>'
                                            f'<li>{product["name"]}, id={product["id"]}, кол-во={product["amount"]}')
    return panel_html


def load_signup_page(signup_html: str, message: str) -> str:
    log(f"Loading signup page with message={message}")
    signup_html = signup_html.replace(
        '<div class="login__form"',
        f'<div class="login__form"> <p class="warning">{message}</p>'
    )
    return signup_html


def load_login_page(login_html: str, message: str) -> str:
    log(f"Loading login page with message={message}")
    login_html = login_html.replace(
        '<div class="login__form"',
        f'<div class="login__form"> <p class="warning">{message}</p>'
    )
    return login_html


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
    total = basket_list.get("total")
    products = basket_list.get("products")
    basket_html = basket_html.replace('</div></body>', f'<p class="name">{name}</p>'
                                                       f'<p class="basket__title">Ваша корзина:</p></div></body>')
    if message is not None:
        basket_html = basket_html.replace(
            '<p class="basket__title">',
            f'<p class="name warning">{message}</p><p class="basket__title">'
        )
    for product_name, price_and_amount in products.items():
        price = price_and_amount["price"]
        amount = price_and_amount["amount"]
        basket_html = basket_html.replace('</div></body>', f'<div class="basket__product">'
                                                     f'<p class="basket__name">{product_name}:</p>'
                                                     f'<p class="product__price">{price}</p>'
                                                     f'<a href="/decrease_from_basket/product={product_name}"'
                                                     f' class="basket__link">'
                                                     f'<img src="static/images/minus.png" alt="" '
                                                     f'height="25px" width="25px"></a> '
                                                     f'<p class="product__amount"> {amount} </p> '
                                                     f'<a href="/increase_from_basket/product={product_name}" '
                                                     f'class="basket__link">'
                                                     f'<img src="static/images/plus.png" alt="" '
                                                     f'height="25px" width="25px"></a></div></div></body>')
    basket_html = basket_html.replace('</div></body>', f'<p class="total__price">Итого: {total}</p>'
                                                 f'<div class="promo">'
                                                 f'<form action="/order" method="post" class="basket__form">'
                                                 f'<p class="promo__title"><strong>ПРОМОКОДЫ:</strong></p>'
                                                 f'<p><input type="radio" id="no" name="promocode" value="no" checked>'
                                                 f'<label for="no">(нет)</label></p>'
                                                 f'<input type="submit" value="Заказать" class="basket__button"/>'
                                                       f'</div></div></body>')
    if promocodes is not None:
        for promo, sale in promocodes.items():
            basket_html = basket_html.replace('<label for="no">(нет)</label></p>',
                                              '<label for="no">(нет)</label></p>'
                                              f'<input type="radio" id="{promo}" name="promocode" value="{promo}">'
                                              f'<label for="{promo}">{sale} руб.</label></p>')
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

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


def load_main_page(index_html: str, products: list[dict], is_authorized: bool = False, username: str = None) -> str:
    log(f"Updating main page with {len(products)} products for user with name={username}")
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

        product_col = product_col.replace(
            'class="product__image" src=',
            f'class="product__image" src="{row["logo_file"]}"'
        )
        product_col = product_col.replace(
            '<div class="product__name">',
            f'<div class="product__name">{row["product_name"]}'
        )
        product_col = product_col.replace(
            '<div class="product__date">',
            f'<div class="product__date">{row["dev_date"]}'
        )
        product_col = product_col.replace(
            'data-modal=',
            f'data-modal=#modal_product_{row["product_id"]}'
        )

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

    if is_authorized:
        index_html = index_html.replace(
            '<div class="header__icons">',
            f'<div class="header__icons"><a href="auth/logout"><img src="static/images/logout.png" alt="" height="41px" width="41px"> </a> '
        )
        index_html = index_html.replace(
            '</nav>',
            f'</nav>{username}'
        )
    else:
        index_html = index_html.replace(
            '<a href="#" class="btn  btn__buy">в корзину',
            '<a href="#" class="btn  btn__buy">авторизуйтесь'
        )

    log("Returning up-to-date main page")
    return index_html

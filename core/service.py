from datetime import datetime
import logging
from pathlib import Path
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from cfg import LOGFILE_PATH


def base_logger(msg: str, module_name: str) -> None:
    time = datetime.now().time()
    logging.info(f" {time.strftime('%H:%M:%S')} {module_name}: {msg}")


def create_logger(filename: str) -> None:
    logging.basicConfig(filename=filename, level=logging.INFO)
    logging.info("\n" * 3 + "/" * 50)
    base_logger("Logger initialized", "LOGGER")


def log(message: str) -> None:
    base_logger(msg=message, module_name="SERVICE")


def upload_pages() -> dict:
    log("Uploading pages from disk")
    pages_dict = {}
    files_list = [file for file in Path('pages').iterdir() if file.is_file()]
    for file in files_list:
        pages_dict.update({file.name: file.open("r", encoding='UTF-8').read()})
    log(f"Found {len(pages_dict)} pages at /core/pages")
    return pages_dict


def mount_static_files(app: FastAPI) -> None:
    app.mount("/static", StaticFiles(directory="static"), name="static")
    log("Static files was mounted")


def update_main_page(index_html: str, products: list[dict]) -> str:
    log(f"Updating main page with {len(products)} products")
    product_cols = []
    modals = []

    template_file = open("templates/product_template.html", "r")
    product_template = template_file.read()
    template_file.close()

    template_file = open("templates/modal_product_template.html", "r")
    modal_template = template_file.read()
    template_file.close()

    log("Template uploaded")
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
            f'</span>{row["amount_items"]}'
        )

        modal = modal.replace(
            '<div class="modal-work__about-chars">',
            f'<div class="modal-work__about-chars">{row["vg_pg"]} {row["nicotine"]} {row["volume"]}'
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
    log("Returning up-to-date main page")
    return index_html


create_logger(LOGFILE_PATH)

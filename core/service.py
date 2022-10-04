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
    log("App was mounted")


def update_main_page(index_html: str, products: list[dict]) -> str:
    log(f"Updating main page with {len(products)} products")
    product_cols = []
    template_file = open("templates/product_template.html", "r")
    template = template_file.read()
    template_file.close()
    log("Template uploaded")
    for row in products:
        product_col = template
        # print(row["product_id"])
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
        product_cols.append(product_col)
    catalog = " ".join(product_cols)
    index_html = index_html.replace(
        '<div class="catalog">',
        f'<div class="catalog">{catalog}'
    )
    log("Returning up-to-date main page")
    return index_html


create_logger(LOGFILE_PATH)

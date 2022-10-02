from datetime import datetime
import logging
from pathlib import Path
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from cfg import LOGFILE_PATH


def update_main_page(index_html: str, products: list[dict]) -> str:
    product_cols = []
    template_file = open("templates/product_template.html", "r")
    template = template_file.read()
    template_file.close()
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
    return index_html



def upload_pages() -> dict:
    pages_dict = {}
    files_list = [file for file in Path('pages').iterdir() if file.is_file()]
    for file in files_list:
        pages_dict.update({file.name: file.open("r", encoding='UTF-8').read()})
    return pages_dict


def mount_static_files(app: FastAPI) -> None:
    app.mount("/static", StaticFiles(directory="static"), name="static")

def base_logger(msg: str, module_name: str) -> None:
    time = datetime.now().time()
    logging.info(f" {time.strftime('%H:%M:%S')} {module_name}: {msg}")


def create_logger(filename: str) -> None:
    logging.basicConfig(filename=filename, level=logging.INFO)
    logging.info("\n" * 3 + "/" * 50)


create_logger(LOGFILE_PATH)
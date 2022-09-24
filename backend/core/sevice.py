from datetime import datetime
import logging
from pathlib import Path
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles


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

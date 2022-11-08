from datetime import datetime
import logging
from pathlib import Path
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from cfg import LOGFILE_PATH, IN_DOCKER


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
    path = 'core/pages' if IN_DOCKER else 'pages'
    files_list = [file for file in Path(path).iterdir() if file.is_file()]
    for file in files_list:
        pages_dict.update({file.name: file.open("r", encoding='UTF-8').read()})
    log(f"Found {len(pages_dict)} pages at /core/pages")
    return pages_dict


def mount_static_files(app: FastAPI) -> None:
    static_dir = "static" if not IN_DOCKER else "core/static"
    app.mount(f"/static", StaticFiles(directory=static_dir), name="static")
    log("Static files was mounted")


create_logger(LOGFILE_PATH)

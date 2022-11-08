from time import sleep
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import OperationalError
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from core.service import base_logger
from cfg import DB_USER, DB_PASSWORD, DB_DIALECT, DB_DRIVER, HOST_DB, DB_NAME, ECHO_FLAG, IN_DOCKER
from psycopg2 import OperationalError as ps2OperationalError
Base = declarative_base()


def log(message: str) -> None:
    base_logger(msg=message, module_name="DATABASE_INITIALIZATION")


def load_session() -> Session:
    log(f"Loading database session with echo={ECHO_FLAG}")
    if IN_DOCKER:
        sleep(5)  # waiting for starting postgresql in docker
    engine = create_engine(
        f"{DB_DIALECT}+{DB_DRIVER}://{DB_USER}:{DB_PASSWORD}@{HOST_DB}/{DB_NAME}",
        echo=ECHO_FLAG
    )  # создание движка базы данных
    try:
        Base.metadata.create_all(bind=engine)  # создание базы данных
    except (OperationalError, ps2OperationalError):
        log("BASE CONNECTION ERROR!!!")
        raise
    log("Base connected!")
    log("Returning session")
    return Session(bind=engine)

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from cfg import DB_USER, DB_PASSWORD, DB_DIALECT, DB_DRIVER, HOST_DB, DB_NAME, ECHO_FLAG

Base = declarative_base()


def load_session() -> Session:
    engine = create_engine(
        f"{DB_DIALECT}+{DB_DRIVER}://{DB_USER}:{DB_PASSWORD}@{HOST_DB}/{DB_NAME}",
        echo=ECHO_FLAG
    )  # создание движка базы данных
    print(Base.metadata)
    Base.metadata.create_all(bind=engine)  # создание базы данных
    return Session(bind=engine)

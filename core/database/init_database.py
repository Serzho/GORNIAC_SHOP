from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

Base = declarative_base()


def load_session() -> Session:
    engine = create_engine()  # создание движка базы данных
    Base.metadata.create_all(bind=engine)  # создание базы данных
    return Session(bind=engine)
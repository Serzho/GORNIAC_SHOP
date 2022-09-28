import sys

sys.path.append("database")

from database.init_database import load_session
from database.user_table import User
from database.reservation_table import Reservation
from database.product_table import Product
from database.item_table import Item
from datetime import date


class DatabaseHandler:
    __session = None

    def __init__(self) -> None:
        self.__session = load_session()

    def signUp(self, name: str, password: str):

        user = User(name, 0, True, password, False, None, date.today(), None, None, None)
        self.__session.rollback()
        self.__session.add(user)
        self.__session.commit()

    def getUserslist(self):
        for el in self.__session.query(User).all():
            print(el.__dict__)

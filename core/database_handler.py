import sys

sys.path.append("database")

from database.init_database import load_session
from database.user_table import User
from database.reservation_table import Reservation
from database.product_table import Product
from database.item_table import Item
from datetime import date
from core.service import base_logger
from hashlib import sha3_256


def log(message: str) -> None:
    module_name = "DBHANDLER"
    base_logger(msg=message, module_name=module_name)


class DatabaseHandler:
    __session = None

    def __init__(self) -> None:
        self.__session = load_session()
        log("Session loaded")
        log("Database handler initialized")

    def signUp(self, name: str, password: str) -> (bool, str):
        sha3_256_password = sha3_256(password.encode()).hexdigest()
        log(f"Adding user to database: name={name}, password={sha3_256_password}")
        if self.__session.query(User.name).filter(User.name == name).count():
            log(f"User with name {name} already exists!")
            return False, f"User with name {name} already exists!"
        else:
            try:
                user = User(name, 0, True, password, False, None, date.today(), None, None, None)
                self.__session.rollback()
                self.__session.add(user)
                self.__session.commit()
                log("Successfully adding user to database!")
                return True, f"User with name {name} successfully added"
            except Exception as e:
                log(f"UNKNOWN ERROR: {e}")
                return False, e

    def get_product_cols(self) -> list[dict]:
        products = self.__session.query(
            Product.product_id,
            Product.dev_date,
            Product.product_name,
            Product.logo_file
        ).all()
        product_cols = []
        for el in products:
            product_cols.append({
                "product_id": el[0],
                "dev_date": f"{el[1].day}.{el[1].month}.{el[1].year}",
                "product_name": el[2],
                "logo_file": el[3]
            })

        return product_cols

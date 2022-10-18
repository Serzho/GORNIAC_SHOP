import sys

sys.path.append("database")

from database.init_database import load_session
from database.user_table import User
from database.reservation_table import Reservation
from database.product_table import Product
from database.item_table import Item
from datetime import date
from core.service import base_logger


def log(message: str) -> None:
    module_name = "DBHANDLER"
    base_logger(msg=message, module_name=module_name)


class DatabaseHandler:
    __session = None

    def __init__(self) -> None:
        self.__session = load_session()
        log("Session loaded")
        log("Database handler initialized")

    def username_exist(self, username: str) -> bool:
        return bool(self.__session.query(User.name).filter(User.name == username).count())

    def add_user(self, username: str, hashed_password: str) -> (bool, str):
        try:
            user = User(username, 0, True, hashed_password, False, None, date.today(), None, None, None)
            self.__session.rollback()
            self.__session.add(user)
            self.__session.commit()
            log("Successfully adding user to database!")
            return True, f"User with name {username} successfully added"
        except Exception as e:
            log(f"UNKNOWN ERROR: {e}")
            return False, e

    def get_user(self, username: str) -> dict:
        user = self.__session.query(User).filter(User.name == username).first()
        if user is not None:
            return user.__dict__
        else:
            return {}

    def get_product_for_order(self, product_id: int) -> dict:
        query = self.__session.query(Product.product_id, Product.product_name, Product.price, Product.is_active).filter(
            Product.product_id == product_id,
            Product.is_active.is_(True)
        ).first()
        log(f"Returning product for order: product_id={product_id}")
        return {"product_name": query.product_name, "price": query.price}

    def get_product_cols(self) -> list[dict]:
        # TODO: СДЕЛАТЬ НОРМАЛЬНОЕ ОТОБРАЖЕНИЕ ДАТЫ!!!
        log("Getting products from database")
        products = self.__session.query(Product).all()
        product_cols = []
        log(f"Founded {len(products)} products")
        for el in products:
            product_cols.append({
                "product_id": el.product_id,
                "dev_date": f"{el.dev_date.day}.{el.dev_date.month}.{el.dev_date.year}",
                "nicotine": el.nicotine,
                "vg_pg": el.vg_pg,
                "amount_items": el.amount_items,
                "is_demo": el.is_demo,
                "is_active": el.is_active,
                "description": el.description,
                "price": el.price,
                "volume": el.volume,
                "rating": el.rating,
                "product_name": el.product_name,
                "logo_file": el.logo_file
            })

        return product_cols

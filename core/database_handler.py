import sys
sys.path.append("database")
from datetime import datetime
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

    def email_exist(self, email: str):
        return bool(self.__session.query(User.email).filter(User.email == email).count())

    def username_exist(self, username: str) -> bool:
        return bool(self.__session.query(User.name).filter(User.name == username).count())

    def add_user(self, username: str, hashed_password: str, email: str) -> (bool, str):
        try:
            user = User(username, 0, True, hashed_password, False, None, date.today(), None, None, None, email)
            self.__session.rollback()
            self.__session.add(user)
            self.__session.commit()
            log("Successfully adding user to database!")
            return True, f"User with name {username} successfully added"
        except Exception as e:
            log(f"UNKNOWN ERROR: {e}")
            return False, e

    def get_product_id(self, product_name: str) -> int:
        return self.__session.query(Product.product_name, Product.product_id).filter(
            Product.product_name == product_name
        ).first().product_id

    def get_user(self, username: str) -> dict:
        user = self.__session.query(User).filter(User.name == username).first()
        if user is not None:
            return user.__dict__
        else:
            return {}

    def get_product_for_basket(self, product_id: int) -> dict:
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

    def get_amount(self, product_name: str) -> int:
        return self.__session.query(Product.product_name, Product.amount_items).filter(
            Product.product_name == product_name
        ).first().amount_items

    def order_exist(self, order_name: str) -> bool:
        return bool(self.__session.query(Reservation.reservation_name).filter(Reservation.reservation_name == order_name).count())

    def get_user_id(self, username: str) -> int:
        return self.__session.query(User.user_id, User.name).filter(User.name == username).first().user_id

    def add_order(self, username: str, order_name: str, product_name: str, amount: int, sale: int, price: int) -> (bool, str):
        try:
            print(self.get_user_id(username))
            order = Reservation(
                reservation_date=datetime.now(),
                user_id=self.get_user_id(username),
                reservation_name=order_name,
                product_id=self.get_product_id(product_name),
                amount=amount,
                is_completed=False,
                sale=sale,
                total=amount * price - sale
            )
            self.__session.rollback()
            self.__session.add(order)
            self.__session.commit()
            log("Successfully adding order to database!")
            return True, f"Order with name {order_name} successfully added"
        except Exception as e:
            log(f"UNKNOWN ERROR: {e}")
            return False, e

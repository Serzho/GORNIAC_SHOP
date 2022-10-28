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

    def change_user_password(self, username: str, hashed_password: str) -> None:
        log(f"Changing password for user={username}")
        user = self.__session.query(User).filter(User.name == username).first()
        try:
            user.hashed_password = hashed_password
            self.__session.commit()
            log("User password was changed")
        except Exception as e:
            log(f"UNKNOWN ERROR: {e}")

    def change_user_email(self, username: str, email: str) -> None:
        log(f"Changing email for user={username}")
        user = self.__session.query(User).filter(User.name == username).first()
        try:
            user.email = email
            self.__session.commit()
            log("User email was changed")
        except Exception as e:
            log(f"UNKNOWN ERROR: {e}")

    def email_exist(self, email: str) -> bool:
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

    def reserve_items(self, product_id: int, amount: int) -> list:
        log(f"Reserve {amount} items of product with id={product_id}")
        reserved_list = []
        items = self.__session.query(Item).filter(
            Item.product_id == product_id, Item.is_reserved.is_not(True)
        ).order_by(Item.manufacture_date).limit(amount).all()
        for item in items:
            try:
                log(f"Trying to reserve item with id={item.item_id}")
                item.is_reserved = True
                self.__session.commit()
                reserved_list.append(item.item_id)
                log(f"Item with id={item.item_id} was reserved")
            except Exception as e:
                log(f"UNKNOWN ERROR: {e}")
        log(f"Returning reserved list with {len(reserved_list)} items")
        return reserved_list

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
        return bool(
            self.__session.query(
                Reservation.reservation_name
            ).filter(Reservation.reservation_name == order_name).count()
        )

    def get_user_id(self, username: str) -> int:
        return self.__session.query(User.user_id, User.name).filter(User.name == username).first().user_id

    def add_order(
            self, username: str, order_name: str, product_id: int, amount: int, sale: int, price: int,
            reserved_dict: dict) -> (bool, str):
        log("Adding order to database")
        try:
            order = Reservation(
                reservation_date=datetime.now(),
                user_id=self.get_user_id(username),
                reservation_name=order_name,
                product_id=product_id,
                amount=amount,
                is_completed=False,
                sale=sale,
                total=amount*price - sale,
                items_reserved=reserved_dict
            )
            log(f"ORDER: {order.__dict__}")
            self.__session.rollback()
            self.__session.add(order)
            self.__session.commit()
            log("Successfully adding order to database!")
            return True, f"Order with name {order_name} successfully added"
        except Exception as e:
            log(f"UNKNOWN ERROR: {e}")
            return False, e

    def get_user_email(self, username: str) -> str:
        return self.__session.query(User.email, User.name).filter(User.name == username).first().email

    def refresh_amount_items(self, product_id: int):
        log(f"Refreshing amount items for product with id={product_id}")
        product = self.__session.query(Product).filter(Product.product_id == product_id).first()
        try:
            product.amount_items = self.__session.query(Item.is_reserved).filter(Item.is_reserved.is_not(True)).count()
            self.__session.commit()
            log(f"Amount items for product with id={product_id} was refreshed")
        except Exception as e:
            log(f"UNKNOWN ERROR: {e}")

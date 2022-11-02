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
from sqlalchemy.orm.attributes import flag_modified


def log(message: str) -> None:
    module_name = "DBHANDLER"
    base_logger(msg=message, module_name=module_name)


class DatabaseHandler:
    __session = None

    def __init__(self) -> None:
        self.__session = load_session()
        log("Session loaded")
        log("Database handler initialized")

    def check_ban_user(self, username: str) -> bool:
        return self.__session.query(User.name, User.is_banned).filter(User.name == username).first().is_banned

    def add_items(self, product_id: int, count: int) -> None:
        try:
            for i in range(count):
                item = Item(product_id, datetime.now(), False, False)
                self.__session.add(item)
            self.__session.commit()
            self.refresh_amount_items(product_id)
        except Exception as e:
            print(e)

    def ban_user(self, user_id: int, ban_description: str) -> None:
        try:
            user = self.__session.query(User).filter(User.user_id == user_id).first()
            user.is_banned = True
            user.ban_description = ban_description
            self.__session.commit()
            self.cancel_orders_dict(user.reservations)
        except Exception as e:
            print(e)

    def get_username(self, user_id: int) -> str:
        return self.__session.query(User.user_id, User.name).filter(User.user_id == user_id).first().name

    def cancel_order(self, order_name: str) -> None:
        product_list = set()
        reservs_query = self.__session.query(Reservation).filter(
            Reservation.reservation_name == order_name, Reservation.is_completed.is_not(True)
        )
        user_id = reservs_query.first().user_id
        user = self.__session.query(User).filter(user_id == User.user_id).first()
        reserv_index = None
        for index, reserv_name in user.reservations.items():
            if reserv_name == order_name:
                reserv_index = index
                break
        user.reservations.pop(reserv_index)
        flag_modified(user, "reservations")
        for reserv in reservs_query:
            for index_item, item_id in reserv.items_reserved.items():
                item = self.__session.query(Item).filter(Item.item_id == item_id).first()
                item.is_reserved = False
                product_list.add(item.product_id)
            self.__session.delete(reserv)
        try:
            self.__session.commit()
            for product_id in product_list:
                self.refresh_amount_items(product_id)
        except Exception as e:
            print(e)

    def cancel_orders_dict(self, reservations: dict) -> None:
        product_list = set()
        for index, reservation_name in reservations.items():
            reservs_query = self.__session.query(Reservation).filter(
                Reservation.reservation_name == reservation_name, Reservation.is_completed.is_not(True)
            )
            for reserv in reservs_query:
                for index_item, item_id in reserv.items_reserved.items():
                    item = self.__session.query(Item).filter(Item.item_id == item_id).first()
                    item.is_reserved = False
                    product_list.add(item.product_id)
                self.__session.delete(reserv)
        try:
            self.__session.commit()
            for product_id in product_list:
                self.refresh_amount_items(product_id)
        except Exception as e:
            print(e)

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

    def add_product(
            self, nicotine: int, vp_pg: str, product_name: str, description: str,
            logo_file: str, price: int, volume: int, rating: int) -> None:
        product = Product(
            dev_date=date.today(),
            nicotine=nicotine,
            vg_pg=vp_pg,
            amount_items=0,
            is_demo=True,
            is_active=False,
            product_name=product_name,
            description=description,
            logo_file=logo_file,
            price=price,
            volume=volume,
            rating=rating
        )
        try:
            self.__session.rollback()
            self.__session.add(product)
            self.__session.commit()
        except Exception as e:
            log(f"UNKNOWN ERROR: {e}")

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

    def refresh_amount_items(self, product_id: int) -> None:
        log(f"Refreshing amount items for product with id={product_id}")
        product = self.__session.query(Product).filter(Product.product_id == product_id).first()
        try:
            product.amount_items = self.__session.query(
                Item.is_reserved, Item.product_id
            ).filter(Item.is_reserved.is_not(True), Item.product_id == product_id).count()
            if product.amount_items == 0:
                product.is_active = False
            else:
                product.is_active = True
                product.is_demo = False
            self.__session.commit()
            log(f"Amount items for product with id={product_id} was refreshed")
        except Exception as e:
            log(f"UNKNOWN ERROR: {e}")

    def register_order(self, order_name: str, username: str) -> None:
        log(f"Register order={order_name} to user={username}")
        user = self.__session.query(User).filter(User.name == username).first()
        try:
            user.last_reservation_date = date.today()
            reservations = user.reservations
            next_index = 1
            if reservations != {}:
                next_index += max(list(map(int, reservations.keys())))
            else:
                reservations = {}
            reservations.update({next_index: order_name})
            user.reservations = reservations
            flag_modified(user, "reservations")
            self.__session.add(user)
            self.__session.commit()
            log(f"Order {order_name} was registered for user={username}")
        except Exception as e:
            log(f"UNKNOWN ERROR: {e}")

    def get_user_orders(self, username: str) -> dict:
        return self.__session.query(User.name, User.reservations).filter(username == User.name).first().reservations

    def complete_order(self, order_name: str) -> None:
        order_query = self.__session.query(Reservation).filter(Reservation.reservation_name == order_name).all()
        try:
            for order in order_query:
                order.is_completed = True
                self.__session.add(order)
            self.__session.commit()
        except Exception as e:
            log(f"UNKNOWN ERROR: {e}")

    def get_user_info_from_order(self, order_name: str) -> dict:
        user_id = self.__session.query(Reservation.user_id, Reservation.reservation_name).filter(
            Reservation.reservation_name == order_name
        ).first().user_id
        username = self.__session.query(User.user_id, User.name).filter(user_id == User.user_id).first().name
        return {"user_id": user_id, "username": username}

    def get_incomplete_orders(self) -> set:
        names_set = set()
        orders_query = self.__session.query(
            Reservation.reservation_name,
            Reservation.is_completed).filter(
            Reservation.is_completed.is_not(True)
        ).all()
        for order in orders_query:
            names_set.add(order.reservation_name)
        return names_set

    def get_product_name(self, product_id: int) -> str:
        return self.__session.query(
            Product.product_id, Product.product_name
        ).filter(product_id == Product.product_id).first().product_name

    def get_order_dict_for_history(self, order_name: str) -> dict:
        log(f"Getting order dict from database: order={order_name}")
        reservs = self.__session.query(
            Reservation.reservation_date,
            Reservation.reservation_name,
            Reservation.product_id,
            Reservation.amount,
            Reservation.is_completed,
            Reservation.total
        ).filter(Reservation.reservation_name == order_name)
        order_dict = {
            "name": order_name, "date": reservs.first().reservation_date, "is_completed": reservs.first().is_completed
        }
        products = {}
        i, total_price = 0, 0
        for el in reservs:
            i += 1
            products.update({i: {
                "product_name": self.get_product_name(el.product_id),
                "price": el.total,
                "amount": el.amount,
                "total": el.total
            }})
            total_price += el.total
        order_dict.update({"products": products, "total_price": total_price})
        log("Returning order dict")
        return order_dict

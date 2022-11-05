from datetime import datetime
import jwt
from core.service import base_logger
from database_handler import DatabaseHandler
from email_handler import EmailHandler
from cfg import SECRET_JWT


def log(message: str) -> None:
    module_name = "BASKETHANDLER"
    base_logger(msg=message, module_name=module_name)


class BasketHandler:
    basket_dict: dict
    database_handler: DatabaseHandler
    email_handler: EmailHandler

    def __init__(self, database_handler: DatabaseHandler, email_handler: EmailHandler):
        self.basket_dict = {}
        self.database_handler = database_handler
        self.email_handler = email_handler
        log("Basket handler initialized")

    def create_promocode(self, user_id: int, sale: int):
        log(f"Creating new promocode for user={user_id}, sale={sale}")
        username = self.database_handler.get_username(user_id)
        promo_jwt = jwt.encode({"sale": sale, "user": username}, SECRET_JWT, algorithm="HS256").decode('utf-8')
        self.database_handler.add_promo(user_id, sale, promo_jwt)
        log("Promocode was successfully created")

    def get_basket_list(self, name: str) -> dict:
        log(f"Getting basket list for user={name}")
        if self.basket_dict.get(name) is None:
            self.add_basket_list(name)
        return self.basket_dict.get(name)

    def add_basket_list(self, name: str) -> None:
        log(f"Creating new basket list for user={name}")
        self.basket_dict.update({
            name: {"creation_time": datetime.today(), "products": {}, "total": 0}
        }
        )

    def add_product(self, name: str, product_id: int) -> None:
        log(f"Adding product with product_id={product_id} for user with name={name}")
        adding_product = self.database_handler.get_product_for_basket(product_id)
        if adding_product is not None:
            basket_list = self.get_basket_list(name)
            product_list = basket_list.get("products")
            current_product = product_list.get(adding_product["product_name"])
            if current_product is not None:
                new_amount = 1 + product_list[adding_product["product_name"]]["amount"]
            else:
                new_amount = 1
            product_list.update(
                {adding_product["product_name"]: {"price": adding_product["price"], "amount": new_amount}})
            basket_list.update({"total": basket_list.get("total") + adding_product["price"]})
            log(f"Product was added")
        else:
            log(f"Adding product is None!!!")

    def decrease_product(self, name: str, product_name: str) -> None:
        log(f"Removing product with product_name={product_name} for user with name={name}")
        basket_list = self.get_basket_list(name)
        product_list = basket_list.get("products")
        current_product = product_list.get(product_name)
        if current_product is not None:
            last_amount = product_list[product_name]["amount"]
            if last_amount <= 1:
                del product_list[product_name]
            else:
                product_list.get(product_name).update({"amount": last_amount - 1})
            basket_list.update({"total": basket_list.get("total") - current_product["price"]})
        else:
            log(f"Current product with name={product_name} doesn't exist in list")

    @staticmethod
    def decode_promocode(promo: str) -> (int, str):
        log(f"Decoding promocode: {promo}")
        try:
            decoded = jwt.decode(promo.encode('utf-8'), SECRET_JWT, algorithm="HS256")
            log(f"Promocode was decoded: {decoded}")
            return decoded["sale"], decoded["user"]
        except Exception as e:
            log(f"Decoding promocode: UNKNOWN ERROR: {e}, Returning (0, 'none')")
            return 0, "none"

    def check_promocode(self, username: str, promo: str) -> bool:
        _, user_jwt = self.decode_promocode(promo)
        return user_jwt == username and user_jwt != "none"

    def check_order(self, username: str, promo: str) -> (bool, str):
        log(f"Checking order for username with name={username}")
        basket_list = self.get_basket_list(username)
        product_list = basket_list.get("products")
        if not len(product_list):
            return False, "Basket is empty!"
        else:
            for product_name, product_chars in product_list.items():
                if product_chars["amount"] > self.database_handler.get_amount(product_name):
                    return False, f"Invalid amount products: " \
                                  f"only {self.database_handler.get_amount(product_name)} items of {product_name}" \
                                  f" exists!"
            return True, "Correct order!"

    def order(self, username: str, promo: str) -> None:
        log(f"Order for user {username}")
        basket_list = self.get_basket_list(username)
        product_list = basket_list.get("products")
        sale = 0
        if promo != "not" and self.check_promocode(username, promo):
            sale, _ = self.decode_promocode(promo)
        number = 0
        while True:
            order_name = f"#{username}#{datetime.now().strftime('%Y%m%d')}#{number}"
            if not self.database_handler.order_exist(order_name):
                break
            else:
                number += 1
        log(f"Order for user {username}: title={order_name}")
        self.email_handler.send_order_email(order_name, username, self.database_handler.get_user_email(username))
        self.database_handler.register_order(order_name, username)
        for product_name, product_chars in product_list.items():
            product_id = self.database_handler.get_product_id(product_name)
            reserved_list = self.database_handler.reserve_items(
                product_id=product_id,
                amount=product_chars["amount"]
            )
            reserved_dict = {i: reserved_list[i] for i in range(len(reserved_list))}
            self.database_handler.refresh_amount_items(product_id)
            current_sale = product_chars["amount"] * product_chars["price"] \
                if product_chars["amount"] * product_chars["price"] < sale else sale
            sale -= current_sale
            success, response_msg = self.database_handler.add_order(
                username, order_name, product_id, product_chars["amount"], current_sale, product_chars["price"], reserved_dict
            )
            self.database_handler.delete_promo(username, promo)
            log(f"Order={order_name}: product={product_name}, success={success}, msg={response_msg}")

    def get_orders_list(self, username: str) -> list:
        log(f"Getting orders list for user={username}")
        orders_names = self.database_handler.get_user_orders(username)
        orders_list = []
        if orders_names is not None:
            for index, name in orders_names.items():
                orders_list.append(self.database_handler.get_order_dict_for_history(name))
        return orders_list

    def get_incompleted_orders_list(self) -> list:
        orders_names = self.database_handler.get_incomplete_orders()
        orders_list = []
        if orders_names is not None:
            for name in orders_names:
                order_dict = self.database_handler.get_order_dict_for_history(name)
                order_dict.update(self.database_handler.get_user_info_from_order(name))
                orders_list.append(order_dict)
        return orders_list

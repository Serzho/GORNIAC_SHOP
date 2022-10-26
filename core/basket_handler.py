from datetime import datetime
from core.service import base_logger
from database_handler import DatabaseHandler


def log(message: str) -> None:
    module_name = "BASKETHANDLER"
    base_logger(msg=message, module_name=module_name)


class BasketHandler:
    basket_dict: dict
    database_handler = None

    def __init__(self, database_handler: DatabaseHandler):
        self.basket_dict = {}
        self.database_handler = database_handler
        log("Basket handler initialized")

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

    def check_order(self, username) -> (bool, str):
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

    def order(self, username: str) -> None:
        log(f"Order for user {username}")
        basket_list = self.get_basket_list(username)
        product_list = basket_list.get("products")
        number = 0
        while True:
            order_name = f"#{username}#{datetime.now().strftime('%Y%m%d')}#{number}"
            if not self.database_handler.order_exist(order_name):
                break
            else:
                number += 1
        log(f"Order for user {username}: title={order_name}")
        for product_name, product_chars in product_list.items():
            success, response_msg = self.database_handler.add_order(
                username, order_name, product_name, product_chars["amount"], 0, product_chars["price"]
            )
            log(f"Order={order_name}: product={product_name}, success={success}, msg={response_msg}")



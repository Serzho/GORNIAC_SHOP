from datetime import datetime
from core.service import base_logger


def log(message: str) -> None:
    module_name = "BASKETHANDLER"
    base_logger(msg=message, module_name=module_name)


class BasketHandler:
    basket_dict: dict
    database_handler = None

    def __init__(self, database_handler):
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
            product_list.update({adding_product["product_name"]: {"price": adding_product["price"], "amount": new_amount}})
            basket_list.update({"total": basket_list.get("total") + adding_product["price"]})
            log(f"Product was added")
        else:
            log(f"Adding product is None!!!")

    def decrease_product(self, name: str, product_name: str) -> None:
        print(self.basket_dict)
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
        print(self.basket_dict)

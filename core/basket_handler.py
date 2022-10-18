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
        adding_product = self.database_handler.get_product_for_order(product_id)
        if adding_product is not None:
            basket_list = self.get_basket_list(name)
            product_list = basket_list.get("products")
            product_list.update({adding_product["product_name"]: {"price": adding_product["price"], "amount": 1}})
            basket_list.update({"total": basket_list.get("total") + adding_product["price"]})
            log(f"Product was added")
        else:
            log(f"Adding product is None!!!")

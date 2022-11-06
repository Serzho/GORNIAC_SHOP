from datetime import date
from sqlalchemy import Column, Integer, SmallInteger, Date, ForeignKey, Boolean
from init_database import Base


class Item(Base):
    __tablename__ = 'item'
    item_id = Column("item_id", Integer, primary_key=True, autoincrement=True)
    product_id = Column("product_id", SmallInteger, ForeignKey("product.product_id"))
    manufacture_date = Column("manufacture_date", Date)
    is_reserved = Column("is_reserved", Boolean)
    is_sales = Column("is_sales", Boolean)

    def __init__(self, product_id: int, manufacture_date: date, is_reserved: bool, is_sales: bool):
        self.product_id = product_id
        self.manufacture_date = manufacture_date
        self.is_reserved = is_reserved
        self.is_sales = is_sales

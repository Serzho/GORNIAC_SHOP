from sqlalchemy import Column, Integer, SmallInteger, Date, ForeignKey
from init_database import Base
from datetime import date


class Item(Base):
    __tablename__ = 'item'
    item_id = Column("item_id", Integer, primary_key=True, autoincrement=True)
    product_id = Column("product_id", SmallInteger, ForeignKey("product.product_id"))
    manufacture_date = Column("manufacture_date", Date)

    def __init__(self, product_id: int, manufacture_date: date):
        self.product_id = product_id
        self.manufacture_date = manufacture_date

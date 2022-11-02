from sqlalchemy import Column, VARCHAR, Boolean, SmallInteger, Date
from init_database import Base
from datetime import date


class Product(Base):
    __tablename__ = 'product'
    product_id = Column("product_id", SmallInteger, primary_key=True, autoincrement=True)
    dev_date = Column("dev_date", Date)
    nicotine = Column("nicotine", SmallInteger)
    vg_pg = Column("vg_pg", VARCHAR(8))
    amount_items = Column("amount_items", SmallInteger)
    is_demo = Column("is_demo", Boolean)
    is_active = Column("is_active", Boolean)
    product_name = Column("product_name", VARCHAR(32))
    description = Column("description", VARCHAR(3072))
    logo_file = Column("logo_file", VARCHAR(64))
    price = Column("price", SmallInteger)
    volume = Column("volume", SmallInteger)
    rating = Column("rating", SmallInteger)

    def __init__(self, dev_date: date, nicotine: int,
                 vg_pg: str, amount_items: int, is_demo: bool, is_active: bool,
                 product_name: str, description: str, logo_file: str, price: int,
                 volume: int, rating: int):
        self.dev_date = dev_date
        self.nicotine = nicotine
        self.vg_pg = vg_pg
        self.amount_items = amount_items
        self.is_demo = is_demo
        self.is_active = is_active
        self.product_name = product_name
        self.description = description
        self.logo_file = logo_file
        self.price = price
        self.volume = volume
        self.rating = rating

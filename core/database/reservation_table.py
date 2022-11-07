from datetime import date
from sqlalchemy import Column, Integer, VARCHAR, Boolean, SmallInteger, Date, ForeignKey, JSON
from core.database.init_database import Base


class Reservation(Base):
    __tablename__ = 'reservation'
    reservation_id = Column("reservation_id", Integer, primary_key=True, autoincrement=True)
    reservation_date = Column("reservation_date", Date)
    user_id = Column("user_id", Integer)
    reservation_name = Column("reservation_name", VARCHAR(32))
    product_id = Column("product_id", SmallInteger, ForeignKey("product.product_id"))
    amount = Column("amount", SmallInteger)
    is_completed = Column("is_completed", Boolean)
    total = Column("total", SmallInteger)
    sale = Column("sale", SmallInteger)
    items_reserved = Column("items_reserved", JSON)

    def __init__(self, reservation_date: date, user_id: int, reservation_name: str,
                 product_id: int, amount: int, is_completed: bool, total: int, sale: int, items_reserved: dict):
        self.reservation_date = reservation_date
        self.user_id = user_id
        self.reservation_name = reservation_name
        self.product_id = product_id
        self.amount = amount
        self.is_completed = is_completed
        self.total = total
        self.sale = sale
        self.items_reserved = items_reserved

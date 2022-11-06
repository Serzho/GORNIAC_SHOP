from datetime import date
import json
from sqlalchemy import Column, Integer, VARCHAR, Boolean, Date, JSON
from core.database.init_database import Base


class User(Base):
    __tablename__ = 'user'
    user_id = Column("user_id", Integer, primary_key=True, autoincrement=True)
    name = Column("name", VARCHAR(32))
    total_purchased = Column("total_purchased", Integer)
    is_active = Column("is_active", Boolean)
    hashed_password = Column("hashed_password", VARCHAR(32))
    is_banned = Column("is_banned", Boolean)
    ban_description = Column("ban_description", VARCHAR(64))
    reg_date = Column("reg_date", Date)
    last_reservation_date = Column("last_reservation_date", Date)
    promo_codes = Column("promo_codes", JSON)
    reservations = Column("reservations", JSON)
    email = Column("email", VARCHAR(64))

    def __init__(self, name: str, total_purchased: int, is_active: bool, hashed_password: str, is_banned: bool,
                 ban_description: str or None, reg_date: date, last_reservation_date: date or None,
                 promo_codes: json or None, reservations: json or None, email: str):
        self.name = name
        self.total_purchased = total_purchased
        self.is_active = is_active
        self.hashed_password = hashed_password
        self.is_banned = is_banned
        self.ban_description = ban_description
        self.reg_date = reg_date
        self.last_reservation_date = last_reservation_date
        self.promo_codes = promo_codes
        self.reservations = reservations
        self.email = email

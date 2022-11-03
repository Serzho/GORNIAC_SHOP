from pydantic import BaseModel
from fastapi import Form
from cfg import SECRET_JWT, JWT_LOCATION


class Request(BaseModel):
    pass


class OrderForm(BaseModel):
    promocode: str

    @classmethod
    def as_form(cls, promocode: str = Form("not")):
        return cls(promocode=promocode)


class AdminAddingPromoForm(BaseModel):
    user_id: int
    sale: int

    @classmethod
    def as_form(cls, user_id: int = Form(-1), sale: int = Form(0)):
        return cls(user_id=user_id, sale=sale)


class AdminAddingItemForm(BaseModel):
    product_id: int
    count: int

    @classmethod
    def as_form(cls, product_id: int = Form(-1), count: int = Form(-1)):
        return cls(product_id=product_id, count=count)


class AdminAddingProductForm(BaseModel):
    nicotine: int
    vp_pg: str
    name: str
    description: str
    logo_file: str
    price: int
    volume: int
    rating: int

    @classmethod
    def as_form(cls, nicotine: int = Form(), vp_pg: str = Form(), name: str = Form(), description: str = Form(),
                logo_file: str = Form(), price: int = Form(), volume: int = Form(), rating: int = Form()):
        return cls(
            nicotine=nicotine, vp_pg=vp_pg, name=name, description=description, logo_file=logo_file,
            price=price, volume=volume, rating=rating)


class AdminBanUserForm(BaseModel):
    user_id: int
    ban_description: str

    @classmethod
    def as_form(cls, user_id: int = Form(), ban_description: str = Form()):
        return cls(user_id=user_id, ban_description=ban_description)


class RequestMessage(BaseModel):
    msg: str


class LoginForm(BaseModel):
    username: str
    password: str

    @classmethod
    def as_form(cls, username: str = Form("empty"), password: str = Form("empty")):
        return cls(username=username, password=password)


class ChangePasswordForm(BaseModel):
    password: str

    @classmethod
    def as_form(cls, password: str = Form("empty")):
        return cls(password=password)


class ChangeEmailForm(BaseModel):
    email: str

    @classmethod
    def as_form(cls, email: str = Form("empty")):
        return cls(email=email)


class SignupForm(BaseModel):
    username: str
    password: str
    email: str

    @classmethod
    def as_form(cls, username: str = Form("empty"), password: str = Form("empty"), email: str = Form("empty")):
        return cls(username=username, password=password, email=email)


class Settings(BaseModel):
    authjwt_secret_key: str = SECRET_JWT
    authjwt_token_location: set = JWT_LOCATION
    authjwt_cookie_csrf_protect: bool = False

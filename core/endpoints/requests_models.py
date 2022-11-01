from pydantic import BaseModel
from fastapi import Form
from cfg import SECRET_JWT, JWT_LOCATION


class Request(BaseModel):
    pass


class AdminAddingItemForm(BaseModel):
    product_id: int
    count: int

    @classmethod
    def as_form(cls, product_id: int = Form(-1), count: int = Form(-1)):
        return cls(product_id=product_id, count=count)


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

from pydantic import BaseModel
from fastapi import Form
from cfg import SECRET_JWT, JWT_LOCATION


class Login_form(BaseModel):
    username: str
    password: str

    @classmethod
    def as_form(cls, username: str = Form(), password: str = Form()):
        return cls(username=username, password=password)


class Signup_page_request(BaseModel):
    message: str | None


class Signup_form(BaseModel):
    username: str
    password: str

    @classmethod
    def as_form(cls, username: str = Form(), password: str = Form()):
        return cls(username=username, password=password)


class Settings(BaseModel):
    authjwt_secret_key: str = SECRET_JWT
    authjwt_token_location: set = JWT_LOCATION
    authjwt_cookie_csrf_protect: bool = False

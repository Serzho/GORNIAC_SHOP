from pydantic import BaseModel
from fastapi import Form
from cfg import SECRET_JWT, JWT_LOCATION


class Request(BaseModel):
    pass


class LoginForm(BaseModel):
    username: str
    password: str

    @classmethod
    def as_form(cls, username: str = Form(), password: str = Form()):
        return cls(username=username, password=password)


class ChangePasswordForm(BaseModel):
    password: str

    @classmethod
    def as_form(cls, password: str = Form()):
        return cls(password=password)


class ChangeEmailForm(BaseModel):
    email: str

    @classmethod
    def as_form(cls, email: str = Form()):
        return cls(email=email)


class SignupForm(BaseModel):
    username: str
    password: str
    email: str

    @classmethod
    def as_form(cls, username: str = Form(), password: str = Form(), email: str = Form()):
        return cls(username=username, password=password, email=email)


class Settings(BaseModel):
    authjwt_secret_key: str = SECRET_JWT
    authjwt_token_location: set = JWT_LOCATION
    authjwt_cookie_csrf_protect: bool = False

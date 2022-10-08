from pydantic import BaseModel
from fastapi import Form


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

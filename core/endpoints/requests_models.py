from pydantic import BaseModel


class Signup_request(BaseModel):
    username: str
    password: str


class Login_request(BaseModel):
    username: str
    password: str
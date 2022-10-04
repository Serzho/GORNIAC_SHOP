from pydantic import BaseModel


class Signup_request(BaseModel):
    name: str
    password: str


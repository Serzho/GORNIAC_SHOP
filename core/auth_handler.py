import jwt
from fastapi import HTTPException
from datetime import datetime, timedelta
from hashlib import sha3_256
from cfg import SECRET


class Auth:
    databaseHandler = None
    secret: str

    def __init__(self, databaseHandler) -> None:
        self.databaseHandler = databaseHandler
        self.secret = SECRET

    def hash_password(self, password: str) -> str:
        return sha3_256(password.encode()).hexdigest()

    def sign_up(self, username: str, password: str) -> (bool, str):
        hashed_password = self.hash_password(password)
        if self.databaseHandler.username_exist(username):
            return False, f"User with name {username} already exists!"
        else:
            return self.databaseHandler.add_user(username, hashed_password)

    def login(self, username: str, password: str) -> (bool, str):
        if not self.databaseHandler.username_exist(username):
            return False, f"User with name {username} doesn't exists!"
        elif self.databaseHandler.get_user()["hashed_password"] == self.hash_password(password):
            return True, "Correct authentication"
        else:
            return False, "Wrong password"

    def encode_token(self, username):
        payload = {
            'exp': datetime.utcnow() + timedelta(days=0, minutes=30),
            'iat': datetime.utcnow(),
            'scope': 'access_token',
            'sub': username
        }
        return jwt.encode(
            payload,
            self.secret,
            algorithm='HS256'
        )

    def decode_token(self, token):
        try:
            payload = jwt.decode(token, self.secret, algorithms=['HS256'])
            if payload['scope'] == 'access_token':
                return payload['sub']
            raise HTTPException(status_code=401, detail='Scope for the token is invalid')
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail='Token expired')
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail='Invalid token')

    def encode_refresh_token(self, username):
        payload = {
            'exp': datetime.utcnow() + timedelta(days=0, hours=10),
            'iat': datetime.utcnow(),
            'scope': 'refresh_token',
            'sub': username
        }
        return jwt.encode(
            payload,
            self.secret,
            algorithm='HS256'
        )

    def refresh_token(self, refresh_token):
        try:
            payload = jwt.decode(refresh_token, self.secret, algorithms=['HS256'])
            if payload['scope'] == 'refresh_token':
                username = payload['sub']
                new_token = self.encode_token(username)
                return new_token
            raise HTTPException(status_code=401, detail='Invalid scope for token')
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail='Refresh token expired')
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail='Invalid refresh token')


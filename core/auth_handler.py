from hashlib import sha3_256


class Auth:
    databaseHandler = None

    def __init__(self, databaseHandler) -> None:
        self.databaseHandler = databaseHandler

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
        elif self.databaseHandler.get_user(username)["hashed_password"] == self.hash_password(password):
            return True, "Correct authentication"
        else:
            return False, "Invalid password"
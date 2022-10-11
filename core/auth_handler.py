from hashlib import sha3_256
from service import base_logger


def log(message: str) -> None:
    module_name = "AUTH_HANDLER"
    base_logger(msg=message, module_name=module_name)


class Auth:
    databaseHandler = None

    def __init__(self, databaseHandler) -> None:
        self.databaseHandler = databaseHandler
        log("Auth handler initialized!")

    @staticmethod
    def hash_password(password: str) -> str:
        log("Hashing password")
        return sha3_256(password.encode()).hexdigest()

    def sign_up(self, username: str, password: str) -> (bool, str):
        hashed_password = self.hash_password(password)
        log(f"Sign up: username={username}, sha_password={hashed_password}")
        if self.databaseHandler.username_exist(username):
            log(f"User with name {username} already exists!")
            return False, f"User with name {username} already exists!"
        else:
            log(f"Adding user with name={username} to database")
            return self.databaseHandler.add_user(username, hashed_password)

    def login(self, username: str, password: str) -> (bool, str):
        log(f"Login user with name={username}")
        if not self.databaseHandler.username_exist(username):
            log(f"User with name {username} doesn't exists!")
            return False, f"User with name {username} doesn't exists!"
        elif self.databaseHandler.get_user(username)["hashed_password"] == self.hash_password(password):
            log(f"Correct authentication user with name={username}")
            return True, "Correct authentication"
        else:
            log(f"Invalid password for user with name={username}")
            return False, "Invalid password"

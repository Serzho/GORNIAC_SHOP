from hashlib import sha3_256
from service import base_logger
from re import match


def log(message: str) -> None:
    module_name = "AUTH_HANDLER"
    base_logger(msg=message, module_name=module_name)


class Auth:
    databaseHandler = None

    def __init__(self, database_handler) -> None:
        self.databaseHandler = database_handler
        log("Auth handler initialized!")

    @staticmethod
    def hash_password(password: str) -> str:
        log("Hashing password")
        return sha3_256(password.encode()).hexdigest()

    def sign_up(self, username: str, password: str, email: str) -> (bool, str):
        if not match(r"^(?=.*[0-9].*)(?=.*[a-z].*)(?=.*[A-Z].*)[0-9a-zA-Z]{8,}$", password):
            return False, f"Too easy password"
        hashed_password = self.hash_password(password)
        log(f"Sign up: username={username}, sha_password={hashed_password}")
        if self.databaseHandler.email_exist(email):
            log(f"Email {email} already used!")
            return False, f"Email {email} already used!"
        elif match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", email) is None:
            log(f"Email isn't correct!")
            return False, f"Email isn't correct!"
        elif self.databaseHandler.username_exist(username):
            log(f"User with name {username} already exists!")
            return False, f"User with name {username} already exists!"
        else:
            log(f"Adding user with name={username} to database")
            return self.databaseHandler.add_user(username, hashed_password, email)

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

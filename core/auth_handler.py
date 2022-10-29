from hashlib import sha3_256
from service import base_logger
from re import match
from database_handler import DatabaseHandler


# TODO: БАГ: ПРОПУСТИЛО БРЕДОВЫЙ ЕМЭИЛ ПРИ РЕГИСТРАЦИИ

def log(message: str) -> None:
    module_name = "AUTH_HANDLER"
    base_logger(msg=message, module_name=module_name)


class Auth:
    databaseHandler = None

    def __init__(self, database_handler: DatabaseHandler) -> None:
        self.databaseHandler = database_handler
        log("Auth handler initialized!")
        log("Creating admin profile")
        self.create_admin()
        log("Admin was created!")

    def change_password(self, username: str, password: str) -> (bool, str):
        log(f"Changing password for user={username}")
        if self.check_password(password):
            self.databaseHandler.change_user_password(username, self.hash_password(password))
            log(f"Password for user={username} changed successfully!")
            return True, "Password was changed"
        else:
            log(f"Password for user={username} didn't changed: password too easy")
            return False, "Password too easy!"

    def change_email(self, username: str, email: str) -> (bool, str):
        log(f"Changing email for user={username}")
        if self.check_email(email):
            self.databaseHandler.change_user_email(username, email)
            log(f"Email for user={username} changed successfully!")
            return True, "Email was changed"
        else:
            log(f"Email for user={username} changed successfully!")
            return False, "Email isn't correct"

    def create_admin(self) -> None:
        log("Creating admin")
        if not self.databaseHandler.username_exist("admin"):
            while True:
                print("Please, enter admin password: ")
                password = input()
                print("Please, enter admin email: ")
                email = input()
                success, msg = self.sign_up("admin", password, email)
                if success:
                    log("Admin profile was created!")
                    break
                else:
                    log(f"Admin profile didn't created: {msg}")
                    print(msg)

    @staticmethod
    def hash_password(password: str) -> str:
        log("Hashing password")
        return sha3_256(password.encode()).hexdigest()

    def sign_up(self, username: str, password: str, email: str) -> (bool, str):
        if not self.check_password(password):
            return False, f"Too easy password"
        hashed_password = self.hash_password(password)
        log(f"Sign up: username={username}, sha_password={hashed_password}")
        if self.databaseHandler.email_exist(email):
            log(f"Email {email} already used!")
            return False, f"Email {email} already used!"
        elif self.check_email(email) is None:
            log(f"Email isn't correct!")
            return False, f"Email isn't correct!"
        elif self.databaseHandler.username_exist(username):
            log(f"User with name {username} already exists!")
            return False, f"User with name {username} already exists!"
        else:
            log(f"Adding user with name={username} to database")
            return self.databaseHandler.add_user(username, hashed_password, email)

    @staticmethod
    def check_email(email: str) -> bool:
        return bool(match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", email))

    @staticmethod
    def check_password(password: str) -> bool:
        return bool(match(r"^(?=.*[0-9].*)(?=.*[a-z].*)(?=.*[A-Z].*)[0-9a-zA-Z]{8,}$", password))

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

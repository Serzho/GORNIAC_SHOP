from re import match
from hashlib import sha3_256
from core.service import base_logger
from core.database_handler import DatabaseHandler


def log(message: str) -> None:
    module_name = "AUTH_HANDLER"
    base_logger(msg=message, module_name=module_name)


class Auth:
    database_handler: DatabaseHandler

    def __init__(self, database_handler: DatabaseHandler) -> None:
        self.database_handler = database_handler
        log("Auth handler initialized!")
        log("Creating admin profile")
        self.__create_admin()
        log("Admin was created!")

    def change_password(self, username: str, password: str) -> (bool, str):
        log(f"Changing password for user={username}")
        if self.check_password(password):
            self.database_handler.change_user_password(username, self.hash_password(password))
            log(f"Password for user={username} changed successfully!")
            return True, "Password was changed"
        else:
            log(f"Password for user={username} didn't changed: password too easy")
            return False, "Password too easy!"

    def change_email(self, username: str, email: str) -> (bool, str):
        log(f"Changing email for user={username}")
        if self.check_email(email):
            self.database_handler.change_user_email(username, email)
            log(f"Email for user={username} changed successfully!")
            return True, "Email was changed"
        else:
            log(f"Email for user={username} changed successfully!")
            return False, "Email isn't correct"

    def __create_admin(self) -> None:
        log("Creating admin")
        if not self.database_handler.username_exist("admin"):
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
        if self.database_handler.email_exist(email):
            log(f"Email {email} already used!")
            return False, f"Email {email} already used!"
        elif self.check_email(email) is None:
            log(f"Email isn't correct!")
            return False, f"Email isn't correct!"
        elif self.database_handler.username_exist(username):
            log(f"User with name {username} already exists!")
            return False, f"User with name {username} already exists!"
        else:
            log(f"Adding user with name={username} to database")
            return self.database_handler.add_user(username, hashed_password, email)

    @staticmethod
    def check_email(email: str) -> bool:
        return bool(match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", email))

    @staticmethod
    def check_password(password: str) -> bool:
        return bool(match(r"^(?=.*[0-9].*)(?=.*[a-z].*)(?=.*[A-Z].*)[0-9a-zA-Z]{8,}$", password))

    def login(self, username: str, password: str) -> (bool, str):
        log(f"Login user with name={username}")
        if not self.database_handler.username_exist(username):
            log(f"User with name {username} doesn't exists!")
            return False, f"User with name {username} doesn't exists!"
        elif self.database_handler.check_ban_user(username):
            return False, "BAN"
        elif self.database_handler.get_user(username)["hashed_password"] == self.hash_password(password):
            log(f"Correct authentication user with name={username}")
            return True, "Correct authentication"
        else:
            log(f"Invalid password for user with name={username}")
            return False, "Invalid password"

    def ban_user(self, user_id: int, ban_description: str) -> None:
        self.database_handler.ban_user(user_id, ban_description)

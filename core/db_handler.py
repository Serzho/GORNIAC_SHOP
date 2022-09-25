from database.init_database import load_session
from database.user_table import User
from datetime import date


class DatabaseHandler:
    __session = None

    def __init__(self) -> None:
        self.__session = load_session()

    def signUp(self, name: str, password: str):
        user = User(name, 0, True, password, False, None, date.today(), None, None, None)
        self.__session.add(user)
        self.__session.commit()

    def getUserslist(self):
        for el in self.__session.query(User).all():
            print(el.__dict__)

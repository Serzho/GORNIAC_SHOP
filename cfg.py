import sys

sys.path.append("core")
sys.path.append("database")

HOST_API = "localhost"
PORT_API = 8000

IN_DOCKER = True

HOST_DB = "postgres" if IN_DOCKER else "localhost"
DB_DIALECT = "postgresql"
PORT_DB = 5432
DB_DRIVER = "psycopg2"

DB_USER = "root"
DB_PASSWORD = "gorniacisgood"
DB_NAME = "gorniac"

PGADMIN_DEFAULT_EMAIL = "kudrsv.kudrsv@gmail.com"
PGADMIN_DEFAULT_PASSWORD = "gorniacadmin"

LOGFILE_PATH = "log.txt"

ECHO_FLAG = False
SECRET_JWT = "GORNIYBODRIY"
JWT_LOCATION = {"cookies"}

EMAIL_HOST = "smtp.mail.ru"
EMAIL = "kudrsv.kudrsv@mail.ru"
EMAIL_PORT = 465
EMAIL_PASS = "DB4rppxQy8buS3EUJ3rV"

ADMIN_PASS = "Gorniacshop12345"
ADMIN_EMAIL = "kudrsv.kudrsv@gmail.com"
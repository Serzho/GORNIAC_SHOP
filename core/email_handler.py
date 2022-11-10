from time import sleep
from threading import Thread
import smtplib
from cfg import EMAIL, EMAIL_HOST, EMAIL_PASS, EMAIL_DELAY
from core.service import base_logger


def log(message: str) -> None:
    module_name = "EMAIL_HANDLER"
    base_logger(msg=message, module_name=module_name)


class EmailHandler(Thread):
    email: str
    password: str
    server: smtplib.SMTP
    __email_query: dict
    is_running: bool

    def __init__(self) -> None:
        self.email = EMAIL
        log("Initializing email handler")
        self.password = EMAIL_PASS
        super().__init__()
        self.__email_query = {}
        self.is_running = True
        log("Email handler initialized")

    def run(self) -> None:
        log("Email handler started")
        while self.is_running:
            if len(self.__email_query):
                for email_id in list(self.__email_query.keys()):
                    log(f"Preparing email with id={email_id}")
                    email_text = self.__email_query.get(email_id).get("text")
                    receiver_email = self.__email_query.get(email_id).get("receiver")
                    log(f"Try to send email with id={email_id}")
                    success = self.__send_email(email_id, email_text, receiver_email)
                    if success:
                        log(f"Deleting email with id={email_id}")
                        del self.__email_query[email_id]
                    else:
                        log("Retrying sending email...")
            else:
                log("Empty query! Waiting...")
                sleep(EMAIL_DELAY)
        log("Email handler stopped")

    def __send_email(self, email_id: int, email_text: str, receiver_email: str) -> bool:
        log(f"Sending email number {email_id}")
        try:
            self.server = smtplib.SMTP_SSL(EMAIL_HOST)
            self.server.login(self.email, self.password)
            self.server.auth_plain()
            self.server.sendmail(self.email, receiver_email, email_text.encode("UTF-8"))
            log(f"Correct sending email number {email_id}")
            return True
        except Exception as e:
            log(f"Sending email: UNKNOWN ERROR: {str(e)}")
            return False

    def add_order_email(self, order_name: str, username: str, receiver_email: str):
        log(f"Adding order email: username={username}, order={order_name} to email={receiver_email}")
        mail_text = f"GORNIAC SHOP \nПривет, {username}!\nСпасибо за ваш заказ: {order_name}"
        email_id = 0 if not len(self.__email_query) else max(self.__email_query.keys()) + 1
        self.__email_query.update({email_id: {"text": mail_text, "receiver": receiver_email}})
        log(f"Correct adding order email: {order_name}, email_id={email_id}")

    def add_ban_email(self, ban_description: str, username: str, receiver_email: str):
        log(f"Adding ban email: username={username}, ban_description={ban_description} to email={receiver_email}")
        mail_text = f"GORNIAC SHOP \nПривет, {username}!\nВы были забанены по причине: {ban_description}"
        email_id = 0 if not len(self.__email_query) else max(self.__email_query.keys()) + 1
        self.__email_query.update({email_id: {"text": mail_text, "receiver": receiver_email}})
        log(f"Correct adding ban email: {username}, email_id={email_id}")

    def add_signup_email(self, username: str, receiver_email: str):
        log(f"Adding signup email: username={username} to email={receiver_email}")
        mail_text = f"GORNIAC SHOP \nПривет, {username}!\nСпасибо за регистрацию, ваш промокод на 50 рублей" \
                    f" уже добавлен, приятных покупок!"
        email_id = 0 if not len(self.__email_query) else max(self.__email_query.keys()) + 1
        self.__email_query.update({email_id: {"text": mail_text, "receiver": receiver_email}})
        log(f"Correct adding signup email: {username}, email_id={email_id}")

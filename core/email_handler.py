import smtplib
from cfg import EMAIL, EMAIL_HOST, EMAIL_PASS
from service import base_logger


def log(message: str) -> None:
    module_name = "EMAILHANDLER"
    base_logger(msg=message, module_name=module_name)


class EmailHandler:
    email: str
    password: str
    server: smtplib.SMTP

    def __init__(self) -> None:
        self.email = EMAIL
        log("Initializing email handler")
        self.password = EMAIL_PASS if EMAIL_PASS else input(f"Please, input email password for {EMAIL}: ")
        log("Email handler initialized")

    def send_order_email(self, order_name: str, username: str, receiver_email: str) -> bool:
        log(f"Sending order email: username={username}, order={order_name} to email={receiver_email}")
        try:
            self.server = smtplib.SMTP_SSL(EMAIL_HOST)
            self.server.login(self.email, self.password)
            self.server.auth_plain()
            mail_text = f"GORNIAC SHOP \nHi, {username}!\nThank u for ur order: {order_name}"
            self.server.sendmail(self.email, receiver_email, mail_text)
            log(f"Correct sending order email: {order_name}")
            return True
        except Exception as e:
            log(str(e))
            return False


if __name__ == "__main__":
    email_handler = EmailHandler()
    email_handler.send_order_email("#fsdsdf#a", "GAY", "kudrsv.kudrsv@gmail.com")


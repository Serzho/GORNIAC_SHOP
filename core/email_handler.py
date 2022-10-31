import smtplib
from cfg import EMAIL, EMAIL_HOST, EMAIL_PASS


class EmailHandler:
    email: str
    password: str
    server: smtplib.SMTP

    def __init__(self):
        self.email = EMAIL
        if not EMAIL_PASS:
            self.password = input(f"Please, input email password for {EMAIL}: ")
        else:
            self.password = EMAIL_PASS
        self.server = smtplib.SMTP_SSL(EMAIL_HOST)
        self.server.login(self.email, self.password)
        self.server.auth_plain()

    def send_order_email(self, order_name: str, username: str, receiver_email: str) -> bool:
        try:
            mail_text = f"GORNIAC SHOP \nHi, {username}!\nThank u for ur order: {order_name}"
            self.server.sendmail(self.email, receiver_email, mail_text)
            return True
        except Exception as e:
            print(e)
            return False


if __name__ == "__main__":
    email_handler = EmailHandler()
    email_handler.send_order_email("#fsdsdf#a", "GAY", "kudrsv.kudrsv@gmail.com")


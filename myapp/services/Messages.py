import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config import Config

CORPORATION_EMAIL = Config.CORPORATION_EMAIL
CORPORATION_PASSWORD = Config.CORPORATION_PASSWORD 
SMTP_SERVER = "smtp.gmail.com"
PORT = 587  

def send_email(recipient_email: str, subject:str, content:str) -> str:
    msg = MIMEMultipart()
    msg["From"] = CORPORATION_EMAIL
    msg["To"] = recipient_email
    msg["Subject"] = subject

    msg.attach(MIMEText(content, "plain"))

    try:
        with smtplib.SMTP(SMTP_SERVER, PORT) as server:
            server.ehlo()               
            server.starttls()           
            server.ehlo()               
            server.login(CORPORATION_EMAIL, CORPORATION_PASSWORD)
            server.sendmail(CORPORATION_EMAIL, recipient_email, msg.as_string())
            return "ok"
    except Exception as e:
        return str(e)


def win_message() -> str:
    pass

def sell_message() -> str:
    pass

def buy_message() -> str:
    pass

def payment_message() -> str:
    pass

def auth_message(email:str, content:str) -> str:
    send_email(
        recipient_email = email,
        subject = "NOTHINK",
        content = "Esse é seu link de autenticação " + content
    )

def change_password_message() -> str:
    pass

def welcome_message() -> str:
    pass


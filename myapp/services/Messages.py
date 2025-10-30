from flask import url_for, current_app
import smtplib
from myapp.utils.Async import make_async
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

@make_async
def win_message() -> str:
    pass

@make_async
def sell_message() -> str:
    pass

@make_async
def buy_message() -> str:
    pass

@make_async
def payment_message() -> str:
    pass

@make_async
def auth_message(email:str, content:str) -> None:
    send_email(
        recipient_email =   email,
        subject =           "AUTENTICAÇÃO - LANCIARE",
        content =           "Esse é seu link de autenticação " + content
    )

@make_async
def welcome_message(email: str, content: str, url:str = None) -> None:
    send_email(
        recipient_email = email,
        subject = "SEJA BEM VINDO - LANCIARE",
        content = f"Seja bem vindo a Lanciare {content}" + f", te encaminhamos um link em que você pode criar uma senha, caso perca o link, você pode a qualquer momento configurá-lo novamente em Esqueci minha senha\nLink: {url}" if url else ""
    )# sorry, but with async just it is possible



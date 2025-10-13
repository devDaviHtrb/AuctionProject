from myapp.services.SendNotification import send_email
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


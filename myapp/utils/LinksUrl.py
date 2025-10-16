from flask import Response, redirect, url_for
SING_IN = "/singIn"
CHANGE_PASSWORD = "/auth/change/"
LOGIN = "/auth/CHANGE_PASSWORD/"

def wait_sing_in() -> Response:
    return redirect(
        url_for(
            "waitingPage.WaitingPage",
            link=SING_IN,
            _external=True
        ),
        code = 303
    )


def wait_change(email:str) -> Response:
    return redirect(
        url_for(
            "waitingPage.WaitingPage",
            link= CHANGE_PASSWORD + email,
            _external=True
            ),
            code = 303
        )
def wait_login(email:str) -> Response:
    return redirect(
        url_for(
            "waitingPage.WaitingPage",
            link= LOGIN + email,
            _external=True
            ),
            code = 303
        )

def profile() -> Response: #user created
    return redirect(url_for("profile.Profile"), code = 303)

def login() -> Response:
    return redirect(url_for("loginPage.LoginPage"), code = 302)

def sing_in() -> Response:
    return redirect(url_for("singInPage.SingInPage"), code = 302)
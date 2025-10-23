from flask import Response, jsonify, redirect, url_for

# -- set consts of pages--
PROFILE_PAGE =          "profilePage.ProfilePage"
WAITING_PAGE =          "waitingPage.WaitingPage"
CHANGE_PASSWORD_PAGE =  "changePasswordPage.ChangePasswordPage"
LOGIN_PAGE =            "loginPage.LoginPage"
SING_UP_PAGE =          "singUpPage.SingUpPage"
CONFIG_PAGE =           "configPage.ConfigPage"
HOME_PAGE =             "homePage.HomePage"

# -- set consts of back-end--
AUTH_GOOGLE_REDIRECT =  "auth.google_redirect"
AUTH_GOOGLE_VALIDATE =  "auth.google_validate"
AUTH_CONFIRM =          "auth.auth"
AUTH_RESEND =           "auth.resend"
AUTH_CHANGE_PASSWORD =  "auth.change_password"

def wait_sing_up() -> Response:
    redirect_url = url_for(
        WAITING_PAGE,
        link=AUTH_RESEND,
        _external=True
    )

    return jsonify({"redirect": redirect_url}), 200


def wait_change(email:str) -> Response:
    return redirect(
        url_for(
                WAITING_PAGE,
            link =      AUTH_RESEND,
            email =     email,
            _external=  True
            )
        )
def wait_login(email:str, ) -> Response:
    redirect_url =url_for(
                WAITING_PAGE,
            link =      AUTH_RESEND,
            email =     email,
            _external=  True
            )
    return jsonify({"redirect": redirect_url}), 200

def change_password(token:str) -> Response:
    return redirect(
        url_for(
            CHANGE_PASSWORD_PAGE,
            token = token
        )
    )

def profile() -> Response: #user created
    redirect_url=url_for(PROFILE_PAGE)

    return jsonify({"redirect": redirect_url}), 200

def login() -> Response:
    return redirect(
        url_for(LOGIN_PAGE)
    )

def sing_up() -> Response:
    return redirect(
        url_for(SING_UP_PAGE)
    )

def configPage() -> Response:
    return redirect(
        url_for(CONFIG_PAGE)
    )

def home() -> Response:
    return redirect(
        url_for(HOME_PAGE)
    )
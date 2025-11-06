from flask import Response, jsonify, redirect, url_for
import myapp.repositories.CategoryRepository as category_repository

# -- set consts of pages--
PROFILE_PAGE =          "configPage.ConfigPage"
WAITING_PAGE =          "waitingPage.WaitingPage"
CHANGE_PASSWORD_PAGE =  "changePasswordPage.ChangePasswordPage"
LOGIN_PAGE =            "homePage.HomePage"
SIGN_UP_PAGE =          "signUpPage.SignUpPage"
CONFIG_PAGE =           "configPage.ConfigPage"
HOME_PAGE =             "homePage.HomePage"
PRODUCTS_PAGE =         "productsPage.ProductsPage"

# -- set consts of back-end--
AUTH_GOOGLE_REDIRECT =  "auth.google_redirect"
AUTH_GOOGLE_VALIDATE =  "auth.google_validate"
AUTH_CONFIRM =          "auth.auth"
AUTH_RESEND =           "auth.resend"
AUTH_CHANGE_PASSWORD =  "auth.change_password"

def wait_sign_up() -> Response:
    redirect_url = url_for(
            WAITING_PAGE,
        link =      AUTH_RESEND,
        _external = True
    )
    return jsonify({"redirect": redirect_url})


def wait_change(email:str) -> Response:
    redirect_url = url_for(
            WAITING_PAGE,
        link =      AUTH_RESEND,
        email =     email,
        _external=  True
    )
    return redirect(redirect_url)
        
def wait_login(email:str) -> Response:
    redirect_url = url_for(
                WAITING_PAGE,
            link =      AUTH_RESEND,
            email =     email,
            _external=  True
            )
    return jsonify({"redirect": redirect_url})

def change_password(token:str) -> Response:
    redirect_url = url_for(
            CHANGE_PASSWORD_PAGE,
            token = token
        )
    return redirect(redirect_url)

def profile() -> Response: #user created
    redirect_url = url_for(PROFILE_PAGE)
    return jsonify( {"redirect": redirect_url})

def login() -> Response:
    redirect_url = url_for(LOGIN_PAGE)
    return redirect(redirect_url)

def sign_up() -> Response:
    redirect_url = url_for(SIGN_UP_PAGE)
    return redirect(redirect_url)

def configPage() -> Response:
    redirect_url = url_for(CONFIG_PAGE)
    return jsonify({"redirect": redirect_url})

def home() -> Response:
    redirect_url = url_for(HOME_PAGE)
    return jsonify({"redirect": redirect_url})

def get_search_links():
    all_categories = category_repository.get_all_name_id()

    links = [(name, f"{url_for(PRODUCTS_PAGE)}?category={name}") for name, _ in all_categories]

    return links
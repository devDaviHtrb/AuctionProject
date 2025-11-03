from flask import session
from myapp.models.Users import users


def init_session(user: users) -> None:
    print(f"foto{user.photo}")
    session["user_photo"] = user.photo if user.photo else "https://res.cloudinary.com/dnet6nodm/image/upload/v1762029407/Users_photos/xlch6finabqgecvcac6r.png"
    session["user_id"] = user.user_id
    session["username"] = user.username
    session["user_wallet"] = user.wallet
    session["admin"] = user.admin_user
    session["email"] = user.email
    session["name"] = user.name

from flask import Blueprint, redirect, request, jsonify, session, url_for, Response
from myapp.models.Users import users
from myapp.utils.LinksUrl import CONFIG_PAGE
from myapp.utils.UploadImage import upload_image
from myapp.setup.InitSqlAlchemy import db
from typing import Tuple
import myapp.repositories.UserRepository as user_repository

changePhoto_bp = Blueprint("changePhoto", __name__)

@changePhoto_bp.route("/changePhoto", methods=["POST"])
def update_profile_photo() -> Tuple[Response, int]:
    try:
        user_id = session.get("user_id")

        file = request.files.get("photo")
        if not file:
            return redirect(url_for(CONFIG_PAGE, msg="Missing Image"))
        
        user = users.query.filter_by(user_id=user_id).first()

        url = upload_image([file], folder="User_photos")
        if not url:
            return redirect(url_for(CONFIG_PAGE, msg="Upload Error"))

        user.photo = url[0]
        db.session.commit()
        session["user_photo"] = url[0]
        return redirect(url_for(CONFIG_PAGE, msg="sucessful")), 200

    except Exception as e:
        return redirect(url_for(CONFIG_PAGE, msg="Internal Error"))

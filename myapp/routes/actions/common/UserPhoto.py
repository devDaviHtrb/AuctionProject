from flask import Blueprint, redirect, request, jsonify, session, url_for
from myapp.utils.LinksUrl import CONFIG_PAGE
from myapp.utils.UploadImage import upload_image
from myapp.models.Users import users
from myapp.setup.InitSqlAlchemy import db

changePhoto_bp = Blueprint("changePhoto", __name__)

@changePhoto_bp.route("/changePhoto", methods=["POST"])
def update_profile_photo():
    try:
        user_id = session.get("user_id")

        file = request.files.get("photo")
        if not file:
            return jsonify({"error": "Missing: image"}), 400


        url = upload_image([file], folder="User_photos")
        if not url:
            return jsonify({"error": "Upload error"}), 500

        # Atualiza no banco
        user = users.query.filter_by(user_id=user_id).first()
        if not user:
            return jsonify({"error": "User not found"}), 404

        user.photo = url[0]
        print(f"foto no change {user.photo}")
        db.session.commit()
        session["user_photo"] = url[0]
        return redirect(url_for(CONFIG_PAGE, msg="sucessful")), 200

    except Exception as e:
        print("❌ Error on update user photo:", e)
        return jsonify({"error": "Internal Error"}), 500
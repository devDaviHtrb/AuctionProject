from flask import Blueprint, render_template

admin_page_bp = Blueprint("adminPage", __name__)

@admin_page_bp.route("/admin")
def AdminPage():
    return render_template(
        "AdminPage.html"
    )
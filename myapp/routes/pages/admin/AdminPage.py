from flask import Blueprint, render_template, Response

admin_page_bp = Blueprint("adminPage", __name__)

@admin_page_bp.route("/admin")
def AdminPage() -> Response:
    return render_template(
        "AdminPage.html"
    )
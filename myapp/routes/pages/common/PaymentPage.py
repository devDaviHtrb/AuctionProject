from flask import Blueprint, session, Response, render_template, redirect, url_for

payment_page_bp = Blueprint("paymentPage", __name__)

@payment_page_bp.route("/payment/choice")
def pay_choice_page() -> Response:
    if("cpf" in session and session.get("cpf", None)):
        return render_template("Payment.html")
    return redirect(url_for("configPage.ConfigPage"))
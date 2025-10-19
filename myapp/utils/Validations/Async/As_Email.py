from flask import url_for
import myapp.services.Messages as msgs

def async_email(email, token):
        try:
            msgs.auth_message(
                email=email,
                content=url_for("auth.auth", token=token, _external=True)
            )
        except Exception as e:
            print("⚠️ Email send error:", e)
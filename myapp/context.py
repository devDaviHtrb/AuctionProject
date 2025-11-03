from flask import session, Flask, url_for
from typing import Dict, Optional, Any
def init_context(app: Flask) -> None:
    @app.context_processor
    def inject_user() -> Dict[str, Optional[Dict[str, Any]]]:
        # pega os links do cache
        search_links = []#_cached_search_links()

        user_id = session.get("user_id")
        if not user_id:
            return dict(user=None)

        user_name = session.get("username")
        user_wallet = session.get("user_wallet")
        user_photo = session.get("user_photo", "#")

        user_context = {
            "id": user_id,
            "photo": user_photo,
            "name": user_name,
            "wallet": user_wallet
        }

        return dict(user=user_context)

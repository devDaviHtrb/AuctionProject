from secrets import token_hex
import threading as thread
from typing import Dict, Any, Optional

pending = {} #{token: user_data}
emails = {} # {email: token}


def add_in(data:Dict[str, Any]) -> str:
    token = token_hex(16)
    pending[token] = data

    emails[data.get("email")] = token

    seconds = 60*60
    timer = thread.Timer(seconds, pop_by_pending, args=[token])
    timer.start()

    return token

def get_by_pending(key:str) -> Optional[Any]:
    return pending.get(key, None)

def get_by_emails_dict(key:str) -> Optional[str]:
    return emails.get(key, None)

def pop_by_pending(key:str) -> None:
    if (not key in pending):
        return
    data = pending.get(key)

    pending.pop(key)
    emails.pop(data.get("email"))
    

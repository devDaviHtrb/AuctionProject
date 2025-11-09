from secrets import token_hex
import threading as thread
from typing import Dict, Any, Optional

#======================= TOKEN =======================
#{
#    token: {
#        "type":         str(sing_in | login | reset)
#        "user_data":    {str: Any}
#    }
#}
#======================================================
pending = {} 
emails = {} # {email: token}


def add_token(data:Dict[str, Any], type: str) -> str:
    token = token_hex(32)
    pending[token] = {
        "type":         type,
        "user_data":    data
    }

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
    data = pending.get(key).get("user_data")
    pending.pop(key)
    emails.pop(data.get("email"))
    

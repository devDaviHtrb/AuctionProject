
from myapp.setup.InitSocket import socketIo
from typing import Dict, Any

@socketIo.on("message")
def Connect(data:Dict[str, Any]) -> None:
    print("Connected")
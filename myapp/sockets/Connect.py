
from myapp.setup.InitSocket import socket_io
from typing import Dict, Any

@socket_io.on("message")
def Connect(data:Dict[str, Any]) -> None:
    print("Connected")

from myapp.setup.InitSocket import socketIo


@socketIo.on("message")
def Connect(data):
    print("Connected")
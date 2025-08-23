from secrets import token_hex


class Config:
    #The constructor method isn't necessary because this class is only a container of static attributes for the server.
    #The attributes are in uppercase in order to follow Flask's standardization.

    SECRET_KEY = token_hex(16)
    SOCKETIO_ASYNC_MODE = "threading"
  
    DEBUG = True
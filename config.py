from secrets import token_hex


class Config:
    #The constructor method isn't necessary because this class is only a container of static attributes for the server.
    #The attributes are in uppercase in order to follow Flask's standardization.

    SECRET_KEY = token_hex(16)
    SOCKETIO_ASYNC_MODE = "threading"
  
    DEBUG = True

    SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://postgres:abc2109@localhost:5432/auction"


    # Evita warnings desnecessários do SQLAlchemy
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
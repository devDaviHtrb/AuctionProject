from dotenv import load_dotenv
from secrets import token_hex
import os

load_dotenv()


class Config:
    #The constructor method isn't necessary because this class is only a container of static attributes for the server.
    #The attributes are in uppercase in order to follow Flask's standardization.

    #API LINK
    URL_API = os.getenv("URL_API")
    SANDBOX_URL_API = os.getenv("SANDBOX_URL_API")

    #API TOKEN
    API_TOKEN = os.getenv("API_TOKEN")
    SANDBOX_API_TOKEN = os.getenv("SANDBOX_API_TOKEN")

    #BANK ID
    ASAAS_WALLET_ID = os.getenv("ASAAS_WALLET_ID")

    #TOKEN FOR OUR API
    INTERNAL_TOKEN_API = os.getenv("INTERNAL_TOKEN_API")

    #EMAIL
    CORPORATION_EMAIL = os.getenv("CORPORATION_EMAIL")
    CORPORATION_PASSWORD = os.getenv("CORPORATION_PASSWORD")
    
    #FLASK
    SECRET_KEY = token_hex(16)
    SOCKETIO_ASYNC_MODE = "threading"  
    DEBUG = True

    SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://postgres:abc2109@localhost:5432/auction"


    # Evita warnings desnecessários do SQLAlchemy
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    

    FLASK_ENV = os.getenv("FLASK_ENV")
    HOST = os.getenv("HOST", "0.0.0.0")
    PORT = os.getenv("PORT", "5000")
    DEBUG = os.getenv("DEBUG", False)

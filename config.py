from dotenv import load_dotenv
from secrets import token_hex
from cryptography.fernet import Fernet
from os import getenv

load_dotenv()


class Config:
    #The constructor method isn't necessary because this class is only a container of static attributes for the server.
    #The attributes are in uppercase in order to follow Flask's standardization.

    #================= API LINK =================
    URL_API =           getenv("URL_API")
    SANDBOX_URL_API =   getenv("SANDBOX_URL_API")
    #============================================

    #================== API TOKEN ==================
    API_TOKEN =         getenv("API_TOKEN")
    SANDBOX_API_TOKEN = getenv("SANDBOX_API_TOKEN")
    #===============================================

    #================== BANK ID ==================
    ASAAS_WALLET_ID =   getenv("ASAAS_WALLET_ID")
    #=============================================

    #================ TOKEN FOR OUR API ================
    INTERNAL_TOKEN_API =    getenv("INTERNAL_TOKEN_API")
    #===================================================

    #======================= EMAIL =======================
    CORPORATION_EMAIL =     getenv("CORPORATION_EMAIL")
    CORPORATION_PASSWORD =  getenv("CORPORATION_PASSWORD")
    GOOGLE_CLIENT_ID =      getenv("GOOGLE_CLIENT_ID")
    GOOGLE_SECRECT =        getenv("GOOGLE_SECRECT")
    GOOGLE_PROJECT_ID =     getenv("GOOGLE_PROJECT_ID")
    GOOGLE_REDIRECT_URIS =  getenv("GOOGLE_REDIRECT_URIS")
    REDIRECT_URI =          getenv("REDIRECT_URI")
    #=====================================================
    
    #============== FLASK ==============
    SOCKETIO_ASYNC_MODE =   "threading"  
    DEBUG =                 True
    #===================================

    #========================= DATABASES =========================
    SQLALCHEMY_DATABASE_URI =   getenv("SQLALCHEMY_DATABASE_URI")
    CLOUDINARY_CLOUD_NAME =     getenv("CLOUDINARY_CLOUD_NAME")
    CLOUDINARY_API_KEY =        getenv("CLOUDINARY_API_KEY")
    CLOUDINARY_API_SECRET =     getenv("CLOUDINARY_API_SECRET")
    #=============================================================

    #=============== KEYS ===============
    SECRET_KEY =    token_hex(32)
    FERNET_KEY =    Fernet.generate_key()
    #====================================

    #=============== LOCAL ===============
    FLASK_ENV = getenv("FLASK_ENV")
    HOST =      getenv("HOST", "0.0.0.0")
    PORT =      getenv("PORT", "5000")
    DEBUG =     getenv("DEBUG", False)
    #=====================================

    # Avoid unnecessary warnings from SQLAlchemy
    SQLALCHEMY_TRACK_MODIFICATIONS =    False
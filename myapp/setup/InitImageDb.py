from os import getenv
import cloudinary 
from dotenv import load_dotenv
from config import Config

CLOUDINARY_CLOUD_NAME = Config.CLOUDINARY_CLOUD_NAME
CLOUDINARY_API_KEY =    Config.CLOUDINARY_API_KEY
CLOUDINARY_API_SECRET = Config.CLOUDINARY_API_SECRET

load_dotenv(".env")
cloudinary.config(
        cloud_name =    CLOUDINARY_CLOUD_NAME,
        api_key =       CLOUDINARY_API_KEY,
        api_secret =    CLOUDINARY_API_SECRET
)

  
    
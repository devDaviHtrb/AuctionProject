from os import getenv
import cloudinary 
from dotenv import load_dotenv
import cloudinary.uploader
import cloudinary.api


load_dotenv(".env")
cloudinary.config(
        cloud_name=getenv("CLOUDINARY_CLOUD_NAME"),
        api_key=getenv("CLOUDINARY_API_KEY"),
        api_secret=getenv("CLOUDINARY_API_SECRET")
)

  
    
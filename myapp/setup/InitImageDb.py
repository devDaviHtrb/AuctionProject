from os import getenv
import cloudinary as image_db
from dotenv import load_dotenv

def init_image_db():

    load_dotenv(".env")
    
    image_db.config(
        cloud_name=getenv("CLOUDINARY_CLOUD_NAME"),
        api_key=getenv("CLOUDINARY_API_KEY"),
        api_secret=getenv("CLOUDINARY_API_SECRET")
    )

    print("👍 image db are on")
    
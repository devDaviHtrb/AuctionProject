from myapp.setup.InitImageDb import cloudinary
from myapp.utils.Async import make_async

@make_async
def async_upload_image(file, data, folder:str) -> bool:
    try:
        file.stream.seek(0) 
        result = cloudinary.uploader.upload(file, folder=folder)
        data["photo_url"] = result["secure_url"]
    except Exception as e:
        print("Cloudinary upload error:", e)

def upload_image(file, folder:str) -> bool:
    try:
        file.stream.seek(0) 
        result = cloudinary.uploader.upload(file, folder=folder)
        return result["secure_url"]
    except Exception as e:
        print("Cloudinary upload error:", e)
        return False
       

    

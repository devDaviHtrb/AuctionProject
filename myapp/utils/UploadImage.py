from myapp.setup.InitImageDb import cloudinary
<<<<<<< HEAD
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
=======
def upload_image(files, folder):
    urls = []
>>>>>>> 6e5a0d657c1488ed806c9f37ba0322dcdbac261e
    try:
        for file in files:
            file.stream.seek(0) 
            result = cloudinary.uploader.upload(file, folder=folder)
            urls.append(result["secure_url"])
        return urls
    except Exception as e:
        print("Cloudinary upload error:", e)
        return False
       

    

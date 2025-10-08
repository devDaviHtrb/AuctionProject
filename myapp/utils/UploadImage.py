import cloudinary

def uploadImage(file, folder):
    try:
        result = cloudinary.uploader.upload(file, folder=folder)
        return result["secure_url"]
    except Exception:
        return False
       

    

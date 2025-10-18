from myapp.setup.InitImageDb import cloudinary
def uploadImage(file, folder):
    try:
        file.stream.seek(0) 
        result = cloudinary.uploader.upload(file.read(), folder=folder)
        return result["secure_url"]
    except Exception as e:
        print("Cloudinary upload error:", e)
        return False
       

    

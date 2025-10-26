from myapp.setup.InitImageDb import cloudinary
def upload_image(files, folder):
    urls = []
    try:
        for file in files:
            file.stream.seek(0) 
            result = cloudinary.uploader.upload(file, folder=folder)
            urls.append(result["secure_url"])
        return urls
    except Exception as e:
        print("Cloudinary upload error:", e)
        return False
       

    

from myapp.utils.UploadImage import uploadImage

def async_upload_image(file, data_dict, folder):
    try:
        photo_url = uploadImage(file, folder)
        if photo_url:
            data_dict["photo_url"] = photo_url
        else:
            print("⚠️ Cloudinary upload failed.")
    except Exception as e:
        print("⚠️ Cloudinary upload error:", e)
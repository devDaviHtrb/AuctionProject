from myapp.utils.UploadImage import upload_image

def async_upload_image(files, data_dict, folder):
    try:
        photos_url = upload_image(files, folder)
        if photos_url:
            data_dict["photos_url"] = photos_url
        else:
            print("⚠️ Cloudinary upload failed.")
    except Exception as e:
        print("⚠️ Cloudinary upload error:", e)
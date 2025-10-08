from PIL import Image
def validateImg(file):
    try:
        img = Image.open(file)
        img.verify()
        return True
    except Exception:
        return False
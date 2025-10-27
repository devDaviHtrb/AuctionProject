from PIL import Image
from werkzeug.datastructures import FileStorage

def validateImg(file: FileStorage) -> bool:
    try:
        img = Image.open(file)
        img.verify()
        return True
    except Exception:
        return False
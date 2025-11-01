from flask import Blueprint, jsonify, request
from myapp.utils.UploadImage import upload_image

HTML = """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Upload de Imagem</title>
</head>
<body>
  <h1>Enviar uma Imagem</h1>
  <form action="/upImage" method="POST" enctype="multipart/form-data">
    <input type="file" name="image" accept="image/*" required>
    <br>
    <input type="submit" value="Enviar Imagem">
  </form>

  <img id="preview" src="" alt="Pré-visualização da imagem" style="display:none;">

  <script>
    const fileInput = document.querySelector('input[name="image"]');
    const preview = document.getElementById('preview');

    fileInput.addEventListener('change', () => {
      const file = fileInput.files[0];
      if (file) {
        const reader = new FileReader();
        reader.onload = (e) => {
          preview.src = e.target.result;
          preview.style.display = 'block';
        }
        reader.readAsDataURL(file);
      } else {
        preview.style.display = 'none';
      }
    });
  </script>
</body>
</html>
"""

up_image_bp = Blueprint("upImage", __name__)

@up_image_bp.route("/upImage", methods=["POST", "GET"])
def receive():
    if request.method == "POST":
        image = request.files.get("image")
        if not image:
            return HTML
        urls = upload_image([image], "Users_photos")
        if not urls:
            return "Erro ao enviar a imagem", 500
        # retorna a URL do Cloudinary para o frontend
        return jsonify(urls)
    return HTML
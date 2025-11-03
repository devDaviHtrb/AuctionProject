const loadingOverlay = document.getElementById('loading-overlay');

function showLoading() {
    loadingOverlay.classList.add('active');
}

function hideLoading() {
    loadingOverlay.classList.remove('active');
}
document.addEventListener('DOMContentLoaded', async () => {
  const fileUpload = document.getElementById('file-upload');
  const previewContainer = document.getElementById('photo-preview-container');
  const categorySelect = document.getElementById('category');
  const dynamicContainer = document.getElementById('category-features');
  let photosFiles = [];

  // --- Mapa de recursos por categoria ---
  let featuresMap = {};
  try {
    const res = await fetch("/get/relationship/categories");
    if (!res.ok) throw new Error("Erro ao buscar categorias");
    featuresMap = await res.json();
    console.log(featuresMap);

    // --- Preenche o select de categorias ---
    Object.keys(featuresMap).forEach(category => {
      const option = document.createElement('option');
      option.value = category;
      option.textContent = category;
      categorySelect.appendChild(option);
    });

  } catch (err) {
    console.error("Erro ao carregar categorias:", err);
  }

  // --- Upload de fotos ---
  fileUpload.addEventListener('change', (e) => {
    const newFiles = Array.from(e.target.files);

    if (photosFiles.length + newFiles.length > 5) {
      alert("Você pode adicionar no máximo 5 fotos.");
      fileUpload.value = '';
      return;
    }

    newFiles.forEach(file => {
      photosFiles.push(file);

      const reader = new FileReader();
      reader.onload = (ev) => {
        const div = document.createElement('div');
        div.classList.add('photo-preview-item');
        div.style.backgroundImage = `url('${ev.target.result}')`;

        const removeBtn = document.createElement('span');
        removeBtn.classList.add('remove-btn');
        removeBtn.innerHTML = '<i class="fas fa-times"></i>';

        removeBtn.addEventListener('click', () => {
          previewContainer.removeChild(div);
          photosFiles = photosFiles.filter(f => f !== file);
        });

        div.appendChild(removeBtn);
        previewContainer.appendChild(div);
      };
      reader.readAsDataURL(file);
    });

    fileUpload.value = '';
  });

  // --- Campos dinâmicos ---
  categorySelect.addEventListener('change', () => {
    dynamicContainer.innerHTML = '';
    const selected = categorySelect.value;
    if (!selected || !featuresMap[selected]) return;

    featuresMap[selected].forEach(feature => {
      const div = document.createElement('div');
      div.classList.add('input-group');

      const label = document.createElement('label');
      label.textContent = feature;
      div.appendChild(label);

      const input = document.createElement('input');
      input.type = 'text';
      input.name = feature.toLowerCase().replace(/\s+/g, '_');
      input.placeholder = feature;
      div.appendChild(input);

      dynamicContainer.appendChild(div);
    });
  });

  // --- Submissão do formulário ---
  const form = document.querySelector('.item-submission-form');
  form.addEventListener('submit', async (e) => {
    e.preventDefault();

    const formData = new FormData(form);

    photosFiles.forEach(file => formData.append('photos', file));

    try {
      const response = await fetch('/new/Auction', {
        method: 'POST',
        body: formData
      });

      if (!response.ok) {
        const err = await response.text();
        throw new Error(err || "Erro no servidor");
      }

      const result = await response.json();
      alert('Item submetido com sucesso!');
      console.log(result);

      form.reset();
      dynamicContainer.innerHTML = '';
      previewContainer.innerHTML = '';
      photosFiles = [];

    } catch (err) {
      console.error(err);
      alert('Erro ao submeter o item.');
    }
  });

});

document.addEventListener('DOMContentLoaded', () => {

  const fileUpload = document.getElementById('file-upload');
  const previewContainer = document.getElementById('photo-preview-container');
  const categorySelect = document.getElementById('category');
  const dynamicContainer = document.getElementById('category-features');
  let photosFiles = [];

  const featuresMap = {
    eletronicos: ['Marca', 'Modelo', 'Ano', 'Garantia'],
    colecionaveis: ['Tipo', 'Material', 'Origem'],
    arte: ['Artista', 'Ano de Criação', 'Estilo', 'Técnica'],
    antiguidades: ['Época', 'Material', 'Procedência', 'Estado de Conservação']
  };

  // --- Upload de fotos ---
  fileUpload.addEventListener('change', (e) => {
    previewContainer.innerHTML = '';
    photosFiles = Array.from(e.target.files);

    if (photosFiles.length > 5) {
      alert("Você pode adicionar no máximo 5 fotos.");
      e.target.value = '';
      photosFiles = [];
      return;
    }

    photosFiles.forEach((file, index) => {
      const reader = new FileReader();
      reader.onload = (ev) => {
        const div = document.createElement('div');
        div.classList.add('photo-preview-item');
        div.style.backgroundImage = `url('${ev.target.result}')`;

        const removeBtn = document.createElement('span');
        removeBtn.classList.add('remove-btn');
        removeBtn.innerHTML = '<i class="fas fa-times"></i>';
        removeBtn.addEventListener('click', () => {
          div.remove();
          photosFiles.splice(index, 1);
        });

        div.appendChild(removeBtn);
        previewContainer.appendChild(div);
      };
      reader.readAsDataURL(file);
    });
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

  // --- Submissão ---
  const form = document.querySelector('.item-submission-form');
  form.addEventListener('submit', async (e) => {
    e.preventDefault();

    const formData = new FormData(form);
    photosFiles.forEach(file => formData.append('photos', file));

    try {
      const response = await postAuction(Object.fromEntries(formData.entries()));
      alert('Item submetido com sucesso!');
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
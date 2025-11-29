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

  let featuresMap = {};
  try {
    const res = await fetch("/get/relationship/categories");
    if (!res.ok) throw new Error("Erro ao buscar categorias");
    featuresMap = await res.json();

    Object.keys(featuresMap).forEach(category => {
      const option = document.createElement('option');
      option.value = category;
      option.textContent = category;
      categorySelect.appendChild(option);
    });

  } catch (err) {
    console.error(err);
  }

  fileUpload.addEventListener('change', (e) => {
    const selectedFiles = Array.from(e.target.files);

    if (photosFiles.length + selectedFiles.length > 5) {
      alert("Você pode adicionar no máximo 5 fotos.");
      fileUpload.value = '';
      return;
    }

    selectedFiles.forEach(file => {
      photosFiles.push(file);

      const reader = new FileReader();
      reader.onload = (ev) => {
        const wrapper = document.createElement('div');
        wrapper.classList.add('photo-preview-item');
        wrapper.style.backgroundImage = `url('${ev.target.result}')`;

        const removeBtn = document.createElement('span');
        removeBtn.classList.add('remove-btn');
        removeBtn.innerHTML = '<i class="fas fa-times"></i>';

        removeBtn.addEventListener('click', () => {
          wrapper.remove();
          photosFiles = photosFiles.filter(f => f !== file);
        });

        wrapper.appendChild(removeBtn);
        previewContainer.appendChild(wrapper);
      };

      reader.readAsDataURL(file);
    });

    e.target.value = '';
  });

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
      input.name = feature;
      input.placeholder = feature;
      div.appendChild(input);

      dynamicContainer.appendChild(div);
    });
  });

  const form = document.querySelector('.item-submission-form');
  form.addEventListener('submit', async (e) => {
    e.preventDefault();

    const formData = new FormData(form);

   
    formData.delete("photos");

  
    photosFiles.forEach(file => formData.append('photos', file));

 
    const startInput = document.getElementById('start-date');
  const startVal = startInput.value;  // ex: "2025-11-25T19:47"

  if (startVal) {

      const withBrazilOffset = `${startVal}:00-03:00`;
      formData.set('start_datetime', withBrazilOffset);
  }


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

      form.reset();
      dynamicContainer.innerHTML = '';
      previewContainer.innerHTML = '';
      photosFiles = [];
      window.location.href = "/";

    } catch (err) {
      console.error(err);
      alert('Erro ao submeter o item.');
    }
  });

});

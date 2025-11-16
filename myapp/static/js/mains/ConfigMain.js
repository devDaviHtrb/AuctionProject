document.addEventListener("DOMContentLoaded", function () {
  const navItems = document.querySelectorAll(".nav-item[data-section]");
  const contentSections = document.querySelectorAll(".settings-section");

  function switchSection(sectionId) {
    contentSections.forEach((s) => {
      s.classList.add("hidden-section");
      s.classList.remove("active-section");
    });

    navItems.forEach((i) => i.classList.remove("active"));

    const target = document.getElementById(sectionId);
    if (target) {
      target.classList.remove("hidden-section");
      target.classList.add("active-section");
    }

    const btn = document.querySelector(`.nav-item[data-section="${sectionId}"]`);
    if (btn) btn.classList.add("active");

    if (sectionId === "bidding") {
      loadBids(1);
    }

    if (sectionId === "security") {
      target.innerHTML = `
        <h2>Segurança</h2>
        <form action="/auth/change" method="POST" class="security-form">
          <label for="email">Email</label>
          <input type="email" name="email" id="email" value="${email}" required>
          <button type="submit">Trocar senha</button>
        </form>
      `;
    }
  }

  navItems.forEach((item) => {
    item.addEventListener("click", (e) => {
      e.preventDefault();
      const sectionId = item.dataset.section;
      if (sectionId) switchSection(sectionId);
    });
  });

  // Inicializa com a seção padrão ou perfil
  switchSection(defaultSection || "profile");

  // Upload de avatar
  const dropzone = document.getElementById("avatar-dropzone");
  const fileInput = document.getElementById("avatar-file");

  if (dropzone && fileInput) {
    dropzone.addEventListener("click", () => fileInput.click());
    dropzone.addEventListener("dragover", (e) => {
      e.preventDefault();
      dropzone.classList.add("dragover");
    });
    dropzone.addEventListener("dragleave", () =>
      dropzone.classList.remove("dragover")
    );
    dropzone.addEventListener("drop", (e) => {
      e.preventDefault();
      dropzone.classList.remove("dragover");
      const file = e.dataTransfer.files[0];
      if (file && file.type.startsWith("image/")) {
        fileInput.files = e.dataTransfer.files;
        const reader = new FileReader();
        reader.onload = (ev) => {
          document.querySelector(".avatar").src = ev.target.result;
        };
        reader.readAsDataURL(file);
      }
    });
  }

  function attachEvents() {
    document.querySelectorAll(".page-btn").forEach((btn) => {
      btn.addEventListener("click", () => {
        const p = Number(btn.dataset.page);
        loadBids(p);
      });
    });
  }

  function loadBids(page = 1) {
    fetch(`/api/bids?page=${page}`)
      .then((r) => r.json())
      .then((data) => {
        let html = "";
        html += `<div class="bids-list">`;

        if (data.bids.length === 0) {
          html += `<p>Você ainda não fez nenhum lance.</p>`;
        }

        for (let b of data.bids) {
          html += `
            <div class="bid-card ${b.status}">
              <div class="bid-info">
                <strong>${b.product_name}</strong><br>
                <span>Lance: R$ ${b.amount.toFixed(2)}</span><br>
                <span>Status: ${b.status}</span>
              </div>
              <div class="bid-link-btn">
                <a href="/produto/${b.room}">Abrir sala</a>
              </div>
            </div>
          `;
        }

        html += `</div>`;

        html += `
          <div class="pagination">
            <a class="page-btn" ${data.page <= 1 ? "style='pointer-events:none;opacity:0.5;'" : ""} data-page="${data.page - 1}">◀</a>
            <span class="page-current">Página ${data.page} de ${data.total_pages}</span>
            <a class="page-btn" ${data.page >= data.total_pages ? "style='pointer-events:none;opacity:0.5;'" : ""} data-page="${data.page + 1}">▶</a>
          </div>
        `;

        document.getElementById("bids-container").innerHTML = html;
        attachEvents();
      });
  }
});

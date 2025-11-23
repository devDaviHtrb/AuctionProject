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


  switchSection(defaultSection || "profile");


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

    // --- AJAX para novo endereço ---
  const newAddressForm = document.getElementById("new-address-form");

  if (newAddressForm) {
    newAddressForm.addEventListener("submit", function (e) {
      e.preventDefault();

      const formData = new FormData(newAddressForm);

      fetch("/new/address", {
        method: "POST",
        body: formData
      })
        .then((r) => r.json())
        .then((data) => {
          if (data.success) {
  
            newAddressForm.reset();

           
            loadAddresses();

          } else {
            alert(data.error || "Erro ao adicionar endereço.");
          }
        })
        .catch(() => alert("Erro inesperado ao enviar o endereço."));
    });
  }
   function loadAddresses() {
    fetch("/api/addresses")
      .then((r) => r.json())
      .then((addresses) => {
        const container = document.getElementById("addresses")
        alert(container.innerText)
        
        let html = `
          <h3>Meus Endereços</h3>
        `;

        if (!addresses.length) {
          html += `<p>Você ainda não possui endereços cadastrados.</p>`;
        } else {
          for (let addr of addresses) {
            html += `
              <div class="address-item">
                <p><strong>${addr.street_name}, ${addr.street_number}</strong> ${addr.apt || ""}</p>
                <p>${addr.district} - ${addr.city}/${addr.state}</p>
                <p>CEP: ${addr.zip_code}</p>
                ${addr.principal_address ? `<p><span class="badge">Principal</span></p>` : ""}

                <form class="remove-address-form" data-id="${addr.address_id}" style="display:inline;">
                  <button type="submit" class="btn-danger">Remover</button>
                </form>
              </div>
            `;
          }
        }

        container.innerHTML = html;

        attachRemoveAddressEvents();
      });
  }


  function attachRemoveAddressEvents() {
    document.querySelectorAll(".remove-address-form").forEach((form) => {
      form.addEventListener("submit", function (e) {
        e.preventDefault();
        const id = form.dataset.id;

        fetch(`/removeAddress/${id}`, {
          method: "POST"
        })
          .then((r) => r.json())
          .then((data) => {
            if (data.success) {
              loadAddresses();
            }
          });
      });
    });
  }
});

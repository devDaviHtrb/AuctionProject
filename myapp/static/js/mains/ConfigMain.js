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

    const btn = document.querySelector(
      `.nav-item[data-section="${sectionId}"]`
    );
    if (btn) btn.classList.add("active");

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

  switchSection("profile");

  navItems.forEach((item) => {
    item.addEventListener("click", (e) => {
      e.preventDefault();
      const sectionId = item.dataset.section;
      if (sectionId) switchSection(sectionId);
    });
  });

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
});

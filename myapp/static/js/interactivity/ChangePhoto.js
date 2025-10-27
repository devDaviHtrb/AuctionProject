document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("photoForm");
  const img = document.getElementById("profilePhoto");
  const msg = document.getElementById("statusMsg");

  form.addEventListener("submit", async (e) => {
    e.preventDefault();

    const fileInput = document.getElementById("photoInput");
    if (!fileInput.files.length) {
      msg.textContent = "Select a image first.";
      return;
    }

    const formData = new FormData();
    formData.append("photo", fileInput.files[0]);

    try {
      msg.textContent = "⏳ Sending...";

      const res = await fetch("/changePhoto", {
        method: "POST",
        body: formData,
        credentials: "include",
      });

      const data = await res.json();

      if (data.success) {
        img.src = data.photo_url;
        msg.textContent = "Ok";
      } else {
        msg.textContent = `⚠️ ${data.error}`;
      }
    } catch (err) {
      msg.textContent = "❌ Request error.";
      console.error(err);
    }
  });
});

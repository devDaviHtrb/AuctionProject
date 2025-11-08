import { login_validation } from "../validations/LogIn.js";
import { login } from "../interactivity/Login.js";

document.addEventListener("DOMContentLoaded", () => {
  const login_cc = document.getElementById("login-cc");
  const buttonSubmit = document.getElementById("submit");
  const message = document.getElementById("message");
  const openLoginBtn = document.getElementById("openLogin");
  const closeLoginBtn = document.getElementById("closeLogin");
  const loginModal = document.getElementById("loginModal");
  const loginForm = document.getElementById("login-form");
  const googleLoginBtn = document.querySelector(".google-login"); 

  if (openLoginBtn && loginModal) {
    openLoginBtn.addEventListener("click", (e) => {
      e.preventDefault();
      loginModal.style.display = "flex";
      setTimeout(() => loginModal.classList.add("show"), 10);
    });
  }

  if (closeLoginBtn) {
    closeLoginBtn.addEventListener("click", closeModal);
  }

  window.addEventListener("click", (e) => {
    if (e.target === loginModal) closeModal();
  });

  function closeModal() {
    loginModal.classList.remove("show");
    setTimeout(() => {
      loginModal.style.display = "none";
    }, 200);
  }

  if (loginForm) {
    loginForm.addEventListener("submit", async (e) => {
      e.preventDefault();
      message.innerHTML = "";

      const username = document.getElementById("login-email").value.trim();
      const password = document.getElementById("login-password").value.trim();

      const isValid = login_validation(username, password, message);
      if (isValid) {
        await login({ username, password });
      }
    });
  }

  if (googleLoginBtn) {
    googleLoginBtn.addEventListener("click", () => {
      window.location.href = "/auth/google/redirect";
    });
  }

});


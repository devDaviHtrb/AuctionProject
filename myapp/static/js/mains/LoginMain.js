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
  const googleLoginBtn = document.querySelector(".google-login"); // novo botão Google

  // === ABRIR MODAL ===
  if (openLoginBtn && loginModal) {
    openLoginBtn.addEventListener("click", (e) => {
      e.preventDefault();
      loginModal.style.display = "flex";
      setTimeout(() => loginModal.classList.add("show"), 10);
    });
  }

  // === FECHAR MODAL (botão X) ===
  if (closeLoginBtn) {
    closeLoginBtn.addEventListener("click", fecharModal);
  }

  // === FECHAR MODAL (clicar fora) ===
  window.addEventListener("click", (e) => {
    if (e.target === loginModal) fecharModal();
  });

  // === FUNÇÃO PARA FECHAR O MODAL COM ANIMAÇÃO ===
  function fecharModal() {
    loginModal.classList.remove("show");
    setTimeout(() => {
      loginModal.style.display = "none";
    }, 200);
  }

  // === ENVIO DO FORMULÁRIO (botão ENTRAR) ===
  if (loginForm) {
    loginForm.addEventListener("submit", async (e) => {
      e.preventDefault(); // impede reload
      message.innerHTML = "";

      const username = document.getElementById("login-email").value.trim();
      const password = document.getElementById("login-password").value.trim();

      const isValid = login_validation(username, password, message);
      if (isValid) {
        await login({ username, password });
      }
    });
  }

  // === BOTÃO GOOGLE LOGIN (redirecionamento simulado) ===
  if (googleLoginBtn) {
    googleLoginBtn.addEventListener("click", () => {
      // Aqui você coloca o redirect real do OAuth Google (exemplo Flask)
      window.location.href = "/auth/google/redirect"; // rota de autenticação
    });
  }

});

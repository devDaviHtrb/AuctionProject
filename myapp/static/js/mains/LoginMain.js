import { login_validation } from "../validations/LogIn.js";
import { login } from "../interactivity/Login.js";

const buttonSubmit = document.getElementById("submit");
const message = document.getElementById("message");
const sign_up = document.getElementById("sign-up");

buttonSubmit.addEventListener("click", async (e) => {
  message.innerHTML = "";

  const username = document.getElementById("login-email").value.trim();
  const password = document.getElementById("login-password").value.trim();

  if (login_validation(username, password, message) == true) {
    await login({ username: username, password: password });
  }
});

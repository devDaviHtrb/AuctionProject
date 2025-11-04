import { login_validation } from "../validations/LogIn.js";
import { login } from "../interactivity/Login.js";

const buttonSubmit = document.getElementById("submit");
const message = document.getElementById("message");
const sign_up = document.getElementById("sign-up");

buttonSubmit.addEventListener("click", async (e) => {
  message.innerHTML = "";

  const username = document.getElementById("username").value.trim();
  const password = document.getElementById("password").value.trim();
  const notRobot = document.getElementById("notRobot").checked;

  if (login_validation(username, password, notRobot, message) == true) {
    await login({ username: username, password: password });
  }
});

sign_up.addEventListener("click", async (e) => {
  window.location.href = sign_up.dataset.url;
})
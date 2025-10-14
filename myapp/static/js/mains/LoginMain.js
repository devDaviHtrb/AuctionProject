import { login_validation } from "../validations/LogIn.js";
import { login } from "../interactivity/Login.js";

const form = document.getElementById("loginForm");
const message = document.getElementById("message");
const forgotPassword = document.getElementById("forgotPassword");

form.addEventListener("submit", (e) => {
  e.preventDefault();
  message.innerHTML = "";

  const username = document.getElementById("username").value.trim();
  const password = document.getElementById("password").value.trim();
  const notRobot = document.getElementById("notRobot").checked;

  if (login_validation(username, password, notRobot, message) == True) {
    login({ username: username, password: password });
  }
});

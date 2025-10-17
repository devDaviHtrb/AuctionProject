import { login_validation } from "../validations/LogIn.js";
import { login } from "../interactivity/Login.js";

const buttonSubmit = document.getElementById("submit");
const message = document.getElementById("message");
const forgotPassword = document.getElementById("forgotPassword");

buttonSubmit.addEventListener("click", async (e) => {
  message.innerHTML = "";

  const username = document.getElementById("username").value.trim();
  const password = document.getElementById("password").value.trim();
  const notRobot = document.getElementById("notRobot").checked;

  if (login_validation(username, password, notRobot, message) == true) {
    await login({ username: username, password: password });
  }
});

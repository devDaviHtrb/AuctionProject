const form = document.getElementById("loginForm");
const message = document.getElementById("message");
const forgotPassword = document.getElementById("forgotPassword");

form.addEventListener("submit", (e) => {
  e.preventDefault();
  message.innerHTML = "";

  const username = document.getElementById("username").value.trim();
  const password = document.getElementById("password").value.trim();
  const notRobot = document.getElementById("notRobot").checked;

  if (!username || !password) {
    message.innerHTML = "Preencha todos os campos.";
    return;
  }

  if (!notRobot) {
    message.innerHTML = "Confirme que você não é um robô.";
    return;
  }

  message.style.color = "green";
  message.innerHTML = "Login realizado com sucesso!";
  form.reset();
});

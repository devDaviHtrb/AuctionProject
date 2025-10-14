export function login_validation(username, password, notRobot, message) {
  if (!username || !password) {
    message.innerHTML = "Preencha todos os campos.";
    return false;
  }

  if (!notRobot) {
    message.innerHTML = "Confirme que você não é um robô.";
    return false;
  }

  return true;
}

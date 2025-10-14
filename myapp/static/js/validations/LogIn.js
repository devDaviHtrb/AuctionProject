export function login_validation(username, password, notRobot, message) {
  if (!username || !password) {
    message.innerHTML = "Preencha todos os campos.";
    return False;
  }

  if (!notRobot) {
    message.innerHTML = "Confirme que você não é um robô.";
    return False;
  }
}

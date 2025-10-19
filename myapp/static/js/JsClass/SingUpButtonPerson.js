import { singUpPerson } from "../interactivity/SingUpPerson";
class LoginButton {
  constructor(id) {
    this.button = document.getElementById(id);

    this.button.addEventListener("click", (event) => {
      singUpPerson();
    });
  }
}

const button = new LoginButton("loginButton");

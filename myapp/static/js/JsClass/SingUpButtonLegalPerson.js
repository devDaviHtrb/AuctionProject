import { singUpLegalPerson } from "../interactivity/SingUpLegalPerson";
class LoginButton {
  constructor(id) {
    this.button = document.getElementById(id);

    this.button.addEventListener("click", (event) => {
      singUpLegalPerson();
    });
  }
}

const button = new LoginButton("loginButton");

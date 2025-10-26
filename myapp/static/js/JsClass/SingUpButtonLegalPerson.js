import { signUpLegalPerson } from "../interactivity/SignUpLegalPerson";
class LoginButton {
  constructor(id) {
    this.button = document.getElementById(id);

    this.button.addEventListener("click", (event) => {
      signUpLegalPerson();
    });
  }
}

const button = new LoginButton("loginButton");

import { signUpPerson } from "../interactivity/SignUpPerson";
class LoginButton {
  constructor(id) {
    this.button = document.getElementById(id);

    this.button.addEventListener("click", (event) => {
      signUpPerson();
    });
  }
}

const button = new LoginButton("loginButton");

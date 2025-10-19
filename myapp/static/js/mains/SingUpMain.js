import { signIn } from "../interactivity/SingUp.js";

document.addEventListener("DOMContentLoaded", () => {
  const signInBtn = document.getElementById("singUpBtn");

  signInBtn.addEventListener("click", async (e) => {
    e.preventDefault();
    const route = window.location.pathname;
    console.log(route);
    await signIn(route);
  });
});

import { signIn } from "../interactivity/SignUp.js";

document.addEventListener("DOMContentLoaded", () => {
  const signInBtn = document.getElementById("signUpBtn");

  signInBtn.addEventListener("click", async (e) => {
    e.preventDefault();
    const route = window.location.pathname;
    console.log(route);
    await signIn(route);
  });
});

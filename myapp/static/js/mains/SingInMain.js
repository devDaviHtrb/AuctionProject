import { signIn } from "../interactivity/SingIn.js";

document.addEventListener("DOMContentLoaded", () => {
  const signInBtn = document.getElementById("singInBtn");

  signInBtn.addEventListener("click", async (e) => {
    e.preventDefault();
    const route = window.location.pathname;
    console.log(route);
    await signIn(route);
  });
});

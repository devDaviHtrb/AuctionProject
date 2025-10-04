import { signIn } from "../interactivity/SingIn";

document.addEventListener("DOMContentLoaded", () => {
  const signInBtn = document.getElementById("signInBtn");

  signInBtn.addEventListener("click", async (e) => {
    e.preventDefault();
    const route = window.location.pathname;
    await signIn(route);
  });
});

export function manageLoginResponse(data) {
  if (data.InputError) {
    document.getElementById("message").innerText = data.InputError;
    document.getElementById("login-cc").style.height = "482px"
    document.getElementById("message").classList.add("active");
  } else if (data.redirect) {
    window.location.href = data.redirect;
  }
}

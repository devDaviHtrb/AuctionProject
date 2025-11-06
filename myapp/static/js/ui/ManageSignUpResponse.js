export function manageSignUpResponse(data) {
  if (data.Type == "InputError") {
    document.getElementById("msg").innerText = data.content;
    console.log(data);
  } else if (data.redirect) {
    window.location.href = data.redirect;
  }
}

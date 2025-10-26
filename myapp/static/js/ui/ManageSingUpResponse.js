export function manageSingUpResponse(data) {
  if (data.Type == "InputError") {
    document.getElementById("message").innerText = data.content;
    console.log(data);
  } else if (data.redirect) {
    window.location.href = data.redirect;
  }
}

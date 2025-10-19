export function manageSingUpResponse(data) {
  if (data.InputError) {
    document.getElementById("message").innerText = data.InputError;
  } else if (data.redirect) {
    window.location.href = data.redirect;
  }
}

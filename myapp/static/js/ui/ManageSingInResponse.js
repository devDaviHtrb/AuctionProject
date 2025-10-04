export function manageSingInResponse(data) {
  if (data.InputError) {
    document.getElementById("msg").innerText = data.InputError;
  } else if (data.redirect) {
    window.location.href = data.redirect;
  }
}

export async function postSingIn(form) {
  const formData = new FormData();
  for (const key in form) {
    formData.append(key, form[key]);
  }

  const request = await fetch("/singIn", {
    method: "POST",
    body: formData,
    credentials: "include",
  });

  return await request.json();
}

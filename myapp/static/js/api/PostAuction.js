export async function postAuction(form) {
  const formData = new FormData();
  for (const key in form) {
    formData.append(key, form[key]);
  }

  const request = await fetch("/new/Auction", {
    method: "POST",
    body: formData,
    credentials: "include",
  });

  return await request.json();
}

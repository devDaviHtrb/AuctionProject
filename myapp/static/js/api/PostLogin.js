export async function postLogin(form) {
  try {
    const request = await fetch("/login", {
      method: "POST",
      body: new URLSearchParams(form),
      credentials: "include",
    });
    const response = await request.json();
    return response;
  } catch (err) {
    console.error("Error on sing in:", err);
    return { error: "Server connection error." };
  }
}

export async function postSingIn(form) {
  try {
    const request = await fetch("/singIn", {
      method: "POST",
      body: new URLSearchParams(form),
      credentials: "include",
    });
    const response = await request.json();
  } catch (err) {
    console.error("Error on sing in:", err);
    return { error: "Server connection error." };
  }
}

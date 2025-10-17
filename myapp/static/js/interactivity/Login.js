import { manageLoginResponse } from "../ui/ManageLoginResponse.js";
import { postLogin } from "../api/PostLogin.js";

export async function login(form) {
  const data = await postLogin(form);
  manageLoginResponse(data);
}

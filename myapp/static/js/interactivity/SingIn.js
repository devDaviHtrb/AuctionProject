import { manageSingInResponse } from "../ui/ManageSingInResponse.js";
import { postSingIn } from "../api/PostSingIn.js";
import { getSingInForm } from "./SingInForm.js";

export async function signIn(route) {
  const form = getSingInForm(route);
  const data = await postSingIn(form);
  manageSingInResponse(data);
}

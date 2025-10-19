import { manageSingUpResponse } from "../ui/ManageSingUpResponse.js";
import { postSingUp } from "../api/PostSingUp.js";
import { getSingUpForm } from "./SingUpForm.js";

export async function signIn(route) {
  const form = getSingUpForm(route);
  const data = await postSingUp(form);
  manageSingUpResponse(data);
}

import { manageSingInResponse } from "../ui/ManageSingInResponse";
import { postSingIn } from "../api/PostSingIn";
import { getSingInForm } from "./SingInForm";

export async function signIn(route) {
  const form = getSingInForm(route);
  const data = await postSingIn(form);
  manageSingInResponse(data);
}

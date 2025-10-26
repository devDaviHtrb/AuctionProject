import { manageSignUpResponse } from "../ui/ManageSignUpResponse.js";
import { postSignUp } from "../api/PostSignUp.js";
import { getSignUpForm } from "./SignUpForm.js";

export async function signIn(route) {
  const form = getSignUpForm(route);
  const data = await postSignUp(form);
  manageSignUpResponse(data);
}

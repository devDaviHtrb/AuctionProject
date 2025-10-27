import { manageSignUpResponse } from "../ui/ManageSignUpResponse.js";
import { postSignUp } from "../api/PostSignUp.js";
import { getSignUpForm } from "./SignUpForm.js";

export async function signIn() {
  const form = getSignUpForm();
  const data = await postSignUp(form);
  manageSignUpResponse(data);
}

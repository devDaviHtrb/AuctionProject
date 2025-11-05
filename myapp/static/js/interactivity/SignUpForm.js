export function getSignUpForm(route) {
  const commomForm = {
    username: document.getElementById("username").value,
    password: document.getElementById("password").value,
    email: document.getElementById("email").value,
    cpf: document.getElementById("cpf").value,
    cellphone1: document.getElementById("cellphone1").value,
  };
  var form = {};
  if (document.getElementById("userType").value == "physical_person") {
    console.log("dsfs foiiii");
    form = {
      ...commomForm,
      name: document.getElementById("name").value,
      userType: "physical_person",
    };
  } else {
    if (document.getElementById("userType").value == "legal_person") {
      form = {
        ...commomForm,
        cnpj: document.getElementById("password").value,
        userType: "legal_person",
      };
    } else {
      console.log("error, this route not exists");
    }
  }
  return form;
}

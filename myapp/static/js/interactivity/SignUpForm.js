export function getSignUpForm(route) {
  const commomForm = {
    username: document.getElementById("username").value,
    password: document.getElementById("password").value,
    email: document.getElementById("email").value,
    cpf: document.getElementById("cpf").value,
    cellphone1: document.getElementById("cellphone1").value,
    cellphone2: document.getElementById("cellphone2").value,
    landline: document.getElementById("landline").value,
    name: document.getElementById("name").value,
  };
  var form = {};
  if (document.getElementById("userType").value == "physical_person") {
    form = {
      ...commomForm,
      userType: "physical_person",
      rg: document.getElementById("rg").value,
      gender: document.getElementById("gender").value,
      birth_date: document.getElementById("birth_date").value,
    };
  } else {
    if (document.getElementById("userType").value == "legal_person") {
      form = {
        ...commomForm,
        legal_business_name: document.getElementById("legal_business_name").value,
        cnpj: document.getElementById("cnpj").value,
        trade_name: document.getElementById("trade_name").value,
        state_tax_registration: document.getElementById("state_tax_registration").value,
        state: document.getElementById("state").value,
        userType: "legal_person",
      };
    } else {
      console.log("error, this route not exists");
    }
  }
  return form;
}

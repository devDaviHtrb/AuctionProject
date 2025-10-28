export function getSignUpForm(route) {
  const commomForm = {
    username: document.getElementById("username").value,
    password: document.getElementById("password").value,
    email: document.getElementById("email").value,
    cpf: document.getElementById("cpf").value,
    cellphone1: document.getElementById("cellphone1").value,
    cellphone2: document.getElementById("cellphone2").value,
    landline: document.getElementById("landline").value,
  };
  var form = {};
  if (document.getElementById("userType").value == "physical_person") {
    console.log("dsfs foiiii");
    form = {
      ...commomForm,
      name: document.getElementById("name").value,
      birth_date: document.getElementById("birth_date").value,
      gender: document.getElementById("gender").value,
      rg: document.getElementById("rg").value,
      userType: "physical_person",
    };
  } else {
    if (document.getElementById("userType").value == "legal_person") {
      form = {
        ...commomForm,
        trade_name: document.getElementById("trade_name").value,
        landline: document.getElementById("landline").value,
        state_tax_registration: document.getElementById(
          "state_tax_registration"
        ).value,
        legal_business_name: document.getElementById("legal_business_name")
          .value,
        scrap_purchase_authorization: document.getElementById(
          "scrap_purchase_authorization"
        ).value,
        cnpj: document.getElementById("password").value,
        userType: "legal_person",
      };
    } else {
      console.log("error, this route not exists");
    }
  }
  return form;
}

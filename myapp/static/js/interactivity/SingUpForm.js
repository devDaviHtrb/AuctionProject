export function getSingUpForm(route) {
  const commomForm = {
    username: document.getElementById("username").value,
    password: document.getElementById("password").value,
    email: document.getElementById("email").value,
    cpf: document.getElementById("cpf").value,
    cellphone1: document.getElementById("cellphone1").value,
    cellphone2: document.getElementById("cellphone2").value,
    landline: document.getElementById("landline").value,
    street_name: document.getElementById("street_name").value,
    street_number: document.getElementById("street_number").value,
    apt: document.getElementById("apt"),
    zip_code: document.getElementById("zip_code").value,
    district: document.getElementById("district").value,
    city: document.getElementById("city").value,
    state: document.getElementById("state").value,
  };
  var form = {};
  if (route.includes("physical")) {
    console.log("dsfs");
    form = {
      ...commomForm,
      name: document.getElementById("name").value,
      birth_date: document.getElementById("birth_date").value,
      gender: document.getElementById("gender").value,
      rg: document.getElementById("rg").value,
      userType: "physical_person",
    };
  } else {
    if (route.includes("legal")) {
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

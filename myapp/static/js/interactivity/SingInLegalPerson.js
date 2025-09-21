export 

function singInLegalPerson(){
fetch("/singIn", {
  method: "POST",
  body: new URLSearchParams({
    username: document.getElementById("username").value,
    password: document.getElementById("password").value,
    email: document.getElementById("email").value,
    cpf: document.getElementById("password").value,
    cnpj: document.getElementById("password").value,
    userType: "legal_person",
    photo: document.getElementById("photo"),
    cellphone1: document.getElementById("cellphone1"),
    cellphone2: document.getElementById("cellphone2"),
    street_name:document.getElementById("street_name"),
    street_number:document.getElementById("street_number"),
    apt:document.getElementById("apt"),
    zip_code:document.getElementById("zip_code"),
    district:document.getElementById("district"),
    city:document.getElementById("city"),
    state:document.getElementById("state"),
    trade_name: document.getElementById("trade_name"),
     landline: document.getElementById("landline").value,
    state_tax_registration: document.getElementById("state_tax_registration"),
    legal_business_name: document.getElementById("legal_business_name"),
    scrap_purchase_authorization:  document.getElementById("scrap_purchase_authorization")

  }),
  credentials: "include"  
})
  .then(res => res.json())
  .then(data => {
    if (data.InputError) {
      document.getElementById("msg").innerText = data.InputError
    } else if (data.redirect) {
      window.location.href = data.redirect;
    }
  });

}
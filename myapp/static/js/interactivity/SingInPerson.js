export 

function singInPerson(){
fetch("/singIn", {
  method: "POST",
  body: new URLSearchParams({
    username: document.getElementById("username").value,
    password: document.getElementById("password").value,
    email: document.getElementById("email").value,
    cpf: document.getElementById("password").value,
    name: document.getElementById("name").value,
    userType: "physical_person",
    photo: document.getElementById("photo"),
    cellphone1: document.getElementById("cellphone1").value,
    cellphone2: document.getElementById("cellphone2").value,
    landline: document.getElementById("landline").value,
    street_name:document.getElementById("street_name").value,
    street_number:document.getElementById("street_number").value,
    apt:document.getElementById("apt").value,
    zip_code:document.getElementById("zip_code").value,
    district:document.getElementById("district").value,
    city:document.getElementById("city").value,
    state:document.getElementById("state").value
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
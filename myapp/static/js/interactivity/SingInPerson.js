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
    userType: "natural person",
    photo: document.getElementById("photo"),
    cellphone1: document.getElementById("cellphone1"),
    cellphone2: document.getElementById("cellphone2"),
    street_name:document.getElementById("street_name"),
    street_number:document.getElementById("street_number"),
    apt:document.getElementById("apt"),
    zip_code:document.getElementById("zip_code"),
    district:document.getElementById("district"),
    city:document.getElementById("city"),
    state:document.getElementById("state")
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
export 

function singInLegalEntity(){
fetch("/singIn", {
  method: "POST",
  body: new URLSearchParams({
    username: document.getElementById("username").value,
    password: document.getElementById("password").value,
    email: document.getElementById("email").value,
    cpf: document.getElementById("password").value,
    cnpj: document.getElementById("password").value,
    userType: "company"

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
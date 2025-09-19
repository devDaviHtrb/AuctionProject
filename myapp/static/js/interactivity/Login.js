export 

function login(){
fetch("/login", {
  method: "POST",
  body: new URLSearchParams({
    username: document.getElementById("username").value,
    password: document.getElementById("password").value
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
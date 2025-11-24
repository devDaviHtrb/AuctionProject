
const form = document.getElementById("signUpForm");
form.addEventListener("submit", (e) => {
  e.preventDefault();
  const formData = new FormData(form);
  const dataObj = Object.fromEntries(formData.entries());

  if (cpfInput.value.replace(/\D/g, "").length !== 11) {
    alert("CPF inválido!");
    return;
  }
  if (rgInput.value.replace(/\D/g, "").length < 8) {
    alert("RG inválido!");
    return;
  }
  if (telefoneInput.value.replace(/\D/g, "").length < 10) {
    alert("Telefone inválido!");
    return;
  }
  if (cepInput.value.replace(/\D/g, "").length !== 8) {
    alert("CEP inválido!");
    return;
  }

  console.log("Dados cadastrados:", dataObj);
  alert("Cadastro realizado com sucesso!");
  form.reset();
});

import { signIn } from "../interactivity/SignUp.js";

document.addEventListener("DOMContentLoaded", () => {
  const signInBtn = document.getElementById("signUpBtn");

  signInBtn.addEventListener("click", async (e) => {
    e.preventDefault();
    await signIn();
  });

  const userTypeSelect = document.getElementById("userType");
  const extraFields = document.getElementById("extraFields");

  userTypeSelect.addEventListener("change", function () {
    const type = this.value;
    extraFields.innerHTML = ""; // limpa o conteúdo anterior

    if (type === "physical_person") {
      extraFields.innerHTML = `
          <label>Nome completo:</label>
          <input type="text" name="name" id="name" required>

          <label>Data de nascimento:</label>
          <input type="date" name="birth_date" id="birth_date" required>

          <label>RG:</label>
          <input type="text" name="rg" id="rg">

          <label>Gênero:</label>
          <select name="gender" id="gender" required>
            <option value="">Selecione</option>
            <option value="feminino">Feminino</option>
            <option value="masculino">Masculino</option>
            <option value="outro">Outro</option>
          </select>
        `;
    } else if (type === "legal_person") {
      extraFields.innerHTML = `

          <label>CNPJ:</label>
          <input type="text" name="cnpj" id="cnpj">
          <label>Razão Social:</label>
          <input type="text" name="razao_social" id="razao_social" required>

          <label>Nome Fantasia:</label>
          <input type="text" name="nome_fantasia" id="nome_fantasia">

          <label>Inscrição Estadual:</label>
          <input type="text" name="inscricao_estadual" id="inscricao_estadual">

          <label>Representante Legal:</label>
          <input type="text" name="representante" id="representante">
        `;
    }
  });
});

document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("signUpForm");
  let steps = Array.from(document.querySelectorAll(".form-step"));
  const progressSteps = Array.from(document.querySelectorAll("#progressBar .step"));
  const userTypeInput = document.getElementById("userType");
  const extraFields = document.getElementById("extraFields");

  // índice da etapa atual (0-based)
  let currentStep = 0;

  // mostra a etapa indexada e atualiza barra de progresso
  function showStep(index) {
    steps.forEach((s, i) => s.classList.toggle("active", i === index));
    progressSteps.forEach((p, i) => p.classList.toggle("active", i <= index));
    currentStep = index;
    // rolar para a etapa visível (opcional)
    steps[index].scrollIntoView({ behavior: "smooth", block: "center" });
  }

  // cria os campos dinâmicos da etapa 4 conforme tipo de usuário
  function renderExtraFieldsFor(type) {
    if (type === "physical_person") {
      extraFields.innerHTML = `
        <label>Nome completo<span class="required">*</span></label>
        <input type="text" name="name" required>

        <label>Data de nascimento<span class="required">*</span></label>
        <input type="date" name="birth_date" required>

        <label>RG</label>
        <input type="text" name="rg">

        <label>Gênero<span class="required">*</span></label>
        <select name="gender" required>
          <option value="">Selecione</option>
          <option value="feminino">Feminino</option>
          <option value="masculino">Masculino</option>
          <option value="outro">Outro</option>
        </select>

        <div class="nav-buttons">
          <button type="button" class="prev-btn">Voltar</button>
          <button type="button" class="next-btn">Próximo</button>
        </div>
      `;
    } else if (type === "legal_person") {
      extraFields.innerHTML = `
        <label>CNPJ<span class="required">*</span></label>
        <input type="text" name="cnpj" required>

        <label>Razão Social<span class="required">*</span></label>
        <input type="text" name="razao_social" required>

        <label>Nome Fantasia<span class="required">*</span></label>
        <input type="text" name="nome_fantasia" required>

        <label>Inscrição Estadual<span class="required">*</span></label>
        <input type="text" name="inscricao_estadual" required>

        <label>Representante Legal<span class="required">*</span></label>
        <input type="text" name="representante" required>

        <div class="nav-buttons">
          <button type="button" class="prev-btn">Voltar</button>
          <button type="button" class="next-btn">Próximo</button>
        </div>
      `;
    } else {
      extraFields.innerHTML = `
        <p>Selecione o tipo de usuário na primeira etapa.</p>
        <div class="nav-buttons">
          <button type="button" class="prev-btn">Voltar</button>
        </div>
      `;
    }
  }

  // valida apenas os campos required da etapa index (0-based).
  // retorna true se válido, false se inválido (foca no primeiro inválido).
  function validateStep(index) {
    const step = steps[index];
    // validação especial: passo 0 (tipo de usuário)
    if (step.dataset.step === "1") {
      if (!userTypeInput.value) {
        alert("Por favor, selecione o tipo de usuário.");
        return false;
      }
    }

    // seleciona inputs/textarea/select com required dentro da etapa atual
    const requiredEls = step.querySelectorAll("input[required], select[required], textarea[required]");
    for (const el of requiredEls) {
      // limpa aparência antiga
      el.classList.remove("invalid");
      if (!el.checkValidity()) {
        // show browser message and focus
        el.reportValidity();
        el.classList.add("invalid");
        el.focus({ preventScroll: true });
        return false;
      }
    }
    return true;
  }

  // valida todo o formulário (usado no submit)
  function validateAll() {
    // render extraFields for current selection to make sure required exist in DOM
    if (userTypeInput.value) renderExtraFieldsFor(userTypeInput.value);

    // primeiro, valida cada etapa que tem requireds
    for (let i = 0; i < steps.length; i++) {
      const step = steps[i];
      const requiredEls = step.querySelectorAll("input[required], select[required], textarea[required]");
      for (const el of requiredEls) {
        if (!el.checkValidity()) {
          // pular para a etapa com o erro e focar
          showStep(i);
          el.reportValidity();
          el.classList.add("invalid");
          el.focus({ preventScroll: true });
          return false;
        }
      }
      // tratamento do tipo de usuário na etapa 1
      if (step.dataset.step === "1" && !userTypeInput.value) {
        showStep(i);
        alert("Selecione o tipo de usuário.");
        return false;
      }
    }

    // última verificação geral do form
    if (!form.checkValidity()) {
      form.reportValidity();
      return false;
    }
    return true;
  }

  // Event delegation: captura clicks em next/prev mesmo quando criados dinamicamente
  form.addEventListener("click", (e) => {
    const target = e.target;

    // Próximo
    if (target.matches(".next-btn")) {
      e.preventDefault();
      // valida a etapa atual antes de avançar
      if (!validateStep(currentStep)) return;

      // se estamos na penúltima etapa e o próximo é o extraFields, renderiza
      const nextIndex = currentStep + 1;

      // antes de mostrar a etapa 3/4, por segurança, renderizar extraFields se form chegar lá
      if (steps[nextIndex] && steps[nextIndex].id === "extraFields") {
        renderExtraFieldsFor(userTypeInput.value);
      }

      if (nextIndex < steps.length) {
        showStep(nextIndex);
      }
      return;
    }

    // Voltar
    if (target.matches(".prev-btn")) {
      e.preventDefault();
      const prevIndex = Math.max(0, currentStep - 1);
      showStep(prevIndex);
      return;
    }

    // seleção do tipo de usuário (botões)
    if (target.matches(".type-btn")) {
      e.preventDefault();
      // ativa visualmente
      document.querySelectorAll(".type-btn").forEach(b => b.classList.remove("active"));
      target.classList.add("active");
      userTypeInput.value = target.dataset.value;
      // se quiser, renderize imediatamente a etapa de extraFields (opcional)
      // renderExtraFieldsFor(userTypeInput.value);
    }
  });

  // submit: valida tudo e só envia se ok
  form.addEventListener("submit", (e) => {
    e.preventDefault();
    if (!validateAll()) {
      return;
    }
    // aqui: todos os campos válidos -> siga com envio via fetch / XHR / form.submit()
    // Exemplo simples:
    // form.submit(); // se quiser submeter normalmente
    console.log("Formulário válido. Preparando envio...");
    // executar envio async (fetch) ou form.submit() conforme sua arquitetura
  });

  // Inicializa: garantir que steps NodeList está correto e mostrar a etapa 0
  steps = Array.from(document.querySelectorAll(".form-step"));
  showStep(0);
});

//recuperação de senha
    forgotPassword.addEventListener("click", (e) => {
      e.preventDefault();
      const emailInput = prompt("Digite seu e-mail para recuperar a senha:");
      if (!emailInput) {
        alert("Você precisa informar um e-mail.");
        return;
      }
      alert("Um link de recuperação foi enviado para " + emailInput);
    });
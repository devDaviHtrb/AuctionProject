
function mascaraCPF(valor) {
  valor = valor.replace(/\D/g, "");
  valor = valor.replace(/(\d{3})(\d)/, "$1.$2");
  valor = valor.replace(/(\d{3})(\d)/, "$1.$2");
  valor = valor.replace(/(\d{3})(\d{1,2})$/, "$1-$2");
  return valor;
}

function mascaraRG(valor) {
  valor = valor.replace(/\D/g, "");
  valor = valor.replace(/(\d{2})(\d)/, "$1.$2");
  valor = valor.replace(/(\d{3})(\d)/, "$1.$2");
  valor = valor.replace(/(\d{3})(\d{1})$/, "$1-$2");
  return valor;
}

function mascaraTelefone(valor) {
  valor = valor.replace(/\D/g, "");
  if (valor.length > 10) {
    valor = valor.replace(/^(\d{2})(\d{5})(\d{4}).*/, "($1) $2-$3");
  } else {
    valor = valor.replace(/^(\d{2})(\d{4})(\d{0,4}).*/, "($1) $2-$3");
  }
  return valor;
}

function mascaraCEP(valor) {
  valor = valor.replace(/\D/g, "");
  valor = valor.replace(/^(\d{5})(\d)/, "$1-$2");
  return valor;
}

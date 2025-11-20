 
    cepInput.addEventListener('blur', async () => {
      const cep = cepInput.value.replace(/\D/g, '');
      if(cep.length === 8){
        try {
          const res = await fetch(`https://viacep.com.br/ws/${cep}/json/`);
          const data = await res.json();
          if(!data.erro){
            ruaInput.value = data.logradouro;
            bairroInput.value = data.bairro;
            cidadeInput.value = data.localidade;
            estadoInput.value = data.uf;
          } else {
            alert("CEP não encontrado!");
          }
        } catch(err){
          alert("Erro ao buscar CEP");
          console.error(err);
        }
      }
    });
function confirmarExclusao() {
    return confirm("Tem certeza que deseja excluir este produto?");
}
async function consultarCEP() {

    const campoCEP = document.getElementById("cep");
    const resultado = document.getElementById("resultado-cep");

    const cep = campoCEP.value.replace(/\D/g, "");

    if (cep.length !== 8) {
        resultado.innerHTML = "<p>Digite um CEP válido com 8 números.</p>";
        return;
    }

    resultado.innerHTML = "<p>Consultando...</p>";

    try {

        const resposta = await fetch(
            `https://viacep.com.br/ws/${cep}/json/`
        );

        const dados = await resposta.json();

        if (dados.erro) {
            resultado.innerHTML = "<p>CEP não encontrado.</p>";
            return;
        }

        resultado.innerHTML = `
            <h3>Endereço encontrado</h3>

            <p><strong>Rua:</strong> ${dados.logradouro}</p>

            <p><strong>Bairro:</strong> ${dados.bairro}</p>

            <p><strong>Cidade:</strong> ${dados.localidade}</p>

            <p><strong>Estado:</strong> ${dados.uf}</p>
        `;

    } catch (erro) {

        resultado.innerHTML =
            "<p>Não foi possível consultar o CEP.</p>";

        console.error(erro);
    }
}
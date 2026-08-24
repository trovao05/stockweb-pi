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
let tamanhoFonte = 16;

function aumentarFonte() {
    tamanhoFonte += 2;
    document.body.style.fontSize = tamanhoFonte + "px";
}

function diminuirFonte() {
    if (tamanhoFonte > 12) {
        tamanhoFonte -= 2;
        document.body.style.fontSize = tamanhoFonte + "px";
    }
}

function alternarContraste() {
    document.body.classList.toggle("alto-contraste");
}

function digitarPorVoz(campoId) {

    const SpeechRecognition =
        window.SpeechRecognition ||
        window.webkitSpeechRecognition;

    if (!SpeechRecognition) {

        alert(
            "O reconhecimento de voz não é compatível com este navegador. " +
            "Tente utilizar Google Chrome ou Microsoft Edge."
        );

        return;
    }

    const reconhecimento = new SpeechRecognition();

    reconhecimento.lang = "pt-BR";
    reconhecimento.interimResults = false;
    reconhecimento.maxAlternatives = 1;

    const campo = document.getElementById(campoId);

    reconhecimento.onstart = function () {

        campo.classList.add("ouvindo");

        campo.setAttribute(
            "placeholder",
            "🎤 Ouvindo..."
        );
    };

    reconhecimento.onresult = function (evento) {

        let texto =
            evento.results[0][0].transcript.trim();

        if (
            campoId === "quantidade" ||
            campoId === "estoque_minimo" ||
            campoId === "preco"
        ) {

            texto = texto
                .replace(",", ".")
                .replace(/[^\d.]/g, "");
        }

        campo.value = texto;
    };

    reconhecimento.onerror = function () {

        alert(
            "Não foi possível reconhecer a fala. Tente novamente."
        );
    };

    reconhecimento.onend = function () {

        campo.classList.remove("ouvindo");

        campo.removeAttribute("placeholder");
    };

    reconhecimento.start();
}

<label for="categoria_existente">
    Categoria
</label>

<select
    id="categoria_existente"
    onchange="alterarTipoCategoria()"
>
    <option value="">
        Selecione uma categoria existente
    </option>

    {% for categoria in categorias_existentes %}

        <option value="{{ categoria }}">
            {{ categoria }}
        </option>

    {% endfor %}

    <option value="__nova__">
        ➕ Digitar nova categoria
    </option>
</select>

<div
    id="area_nova_categoria"
    class="campo-com-voz"
    style="display: none;"
>

    <input
        type="text"
        id="categoria_manual"
        placeholder="Digite a nova categoria. Ex: Informática, Eletrônicos..."
        autocomplete="off"
    >

    <button
        type="button"
        class="botao-voz"
        onclick="digitarPorVoz('categoria_manual')"
        aria-label="Preencher categoria por voz"
        title="Preencher por voz"
    >
        🎤
    </button>

</div>

<input
    type="hidden"
    id="categoria"
    name="categoria"
></input>
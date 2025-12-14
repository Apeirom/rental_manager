/**
 * Controla a visibilidade dos campos de garantia no formulário de contratos.
 * Chamado automaticamente ao carregar a página e quando o usuário muda o select.
 */
function toggleGuaranteeFields() {
    const guaranteeSelect = document.getElementById('guaranteeType');
    
    // Se o elemento não existir na página (ex: estamos em outra tela), para a execução.
    if (!guaranteeSelect) return;

    const type = guaranteeSelect.value;
    
    // Divs containers
    const divCaucao = document.getElementById('divCaucao');
    const divFiador = document.getElementById('divFiador');
    const divSeguro = document.getElementById('divSeguro');
    
    // Inputs internos
    const inputDeposit = document.getElementById('inputDeposit');
    const selectFiador = document.getElementById('selectFiador');
    const selectSeguro = document.getElementById('selectSeguro');

    // 1. Resetar estado: Esconde tudo e desabilita inputs para não enviar lixo
    [divCaucao, divFiador, divSeguro].forEach(el => el.style.display = 'none');
    
    inputDeposit.required = false;
    
    selectFiador.disabled = true;
    selectFiador.required = false;
    
    selectSeguro.disabled = true;
    selectSeguro.required = false;

    // 2. Ativa apenas o bloco escolhido
    if (type === 'caucao') {
        divCaucao.style.display = 'block';
        inputDeposit.required = true;
        // Opcional: focar no campo
        // inputDeposit.focus(); 
    } 
    else if (type === 'fiador') {
        divFiador.style.display = 'block';
        selectFiador.disabled = false;
        selectFiador.required = true;
        inputDeposit.value = "0"; // Garante que depósito seja zero
    } 
    else if (type === 'seguro_fianca') {
        divSeguro.style.display = 'block';
        selectSeguro.disabled = false;
        selectSeguro.required = true;
        inputDeposit.value = "0";
    }
}

// Inicialização:
// Como o HTMX carrega o HTML dinamicamente, o evento 'DOMContentLoaded' normal
// já passou. Precisamos ouvir o evento 'htmx:afterSwap' ou rodar a função manualmente.

// Opção A: Tenta rodar imediatamente (caso o script seja carregado junto)
toggleGuaranteeFields();

// Opção B: Escuta o HTMX para garantir que rode sempre que um novo conteúdo entrar
document.body.addEventListener('htmx:afterSwap', function(event) {
    // Verifica se o novo conteúdo tem o nosso select, se tiver, roda a função
    if (event.target.querySelector('#guaranteeType')) {
        toggleGuaranteeFields();
    }
}); 
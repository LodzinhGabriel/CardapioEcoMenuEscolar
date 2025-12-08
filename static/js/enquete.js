// Elementos do DOM
const opcoes = document.querySelectorAll('.enquete-opcao');
const enviarBtn = document.getElementById('enquete-enviar');
const mensagem = document.getElementById('enquete-mensagem');

// Array para armazenar as opções selecionadas
let diasSelecionados = [];

// Adicionar evento de clique a cada opção
opcoes.forEach(opcao => {
    opcao.addEventListener('click', function() {
        const dia = this.getAttribute('data-dia');
        
        // Verificar se o dia já está selecionado
        const index = diasSelecionados.indexOf(dia);
        
        if (index > -1) {
            // Se já está selecionado, remover
            diasSelecionados.splice(index, 1);
            this.classList.remove('selecionado');
        } else {
            // Se não está selecionado, adicionar
            diasSelecionados.push(dia);
            this.classList.add('selecionado');
        }
    });
});

// Evento de clique no botão enviar
enviarBtn.addEventListener('click', function() {
    // Verificar se pelo menos uma opção foi selecionada
    if (diasSelecionados.length === 0) {
        exibirMensagem('Por favor, selecione pelo menos uma opção.', 'erro');
        return;
    }
    
    // Simular envio dos dados
    // Em um cenário real, você faria uma requisição AJAX aqui
    console.log('Dias selecionados:', diasSelecionados);
    
    // Simular resposta do servidor
    setTimeout(() => {
        exibirMensagem('Obrigado por participar da nossa enquete!', 'sucesso');
        
        // Limpar seleção após 2 segundos
        setTimeout(() => {
            limparSelecao();
            ocultarMensagem();
        }, 2000);
    }, 500);
});

// Função para exibir mensagem
function exibirMensagem(texto, tipo) {
    mensagem.textContent = texto;
    mensagem.className = 'enquete-mensagem ' + tipo;
    mensagem.style.display = 'block';
}

// Função para ocultar mensagem
function ocultarMensagem() {
    mensagem.style.display = 'none';
}

// Função para limpar seleção
function limparSelecao() {
    diasSelecionados = [];
    opcoes.forEach(opcao => {
        opcao.classList.remove('selecionado');
    });
}
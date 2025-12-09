// Elementos do DOM
const opcoes = document.querySelectorAll('.enquete-opcao');
const enviarBtn = document.getElementById('enquete-enviar');
const mensagem = document.getElementById('enquete-mensagem');

// Variável para armazenar a única opção selecionada
let diaSelecionado = null;

// Adicionar evento de clique a cada opção
opcoes.forEach(opcao => {
    opcao.addEventListener('click', function() {
        const dia = this.getAttribute('data-dia');

        // Se já está selecionada, desmarca
        if (diaSelecionado === dia) {
            diaSelecionado = null;
            this.classList.remove('selecionado');
            return;
        }

        // Limpar seleção anterior
        opcoes.forEach(o => o.classList.remove('selecionado'));

        // Marcar nova opção
        diaSelecionado = dia;
        this.classList.add('selecionado');
    });
});

// Evento de clique no botão enviar
enviarBtn.addEventListener('click', function() {
    if (!diaSelecionado) {
        exibirMensagem('Por favor, selecione uma opção.', 'erro');
        return;
    }

    console.log('Dia selecionado:', diaSelecionado);

    const formulario = new FormData()

    formulario.append('dia', diaSelecionado)

    fetch('/enquete/voto', {
        method: 'POST',
        body: formulario,
    })
    .then(res => res.json())
    .then((data) => {
        console.log(data.mensagem || data.erro)

        exibirMensagem(data.mensagem || data.erro, data.erro == null ? 'erro' : 'sucesso');

        // Limpar seleção após 2 segundos
        setTimeout(() => {
            limparSelecao();
            ocultarMensagem();
        }, 2000);
    });
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
    diaSelecionado = null;
    opcoes.forEach(opcao => {
        opcao.classList.remove('selecionado');
    });
}

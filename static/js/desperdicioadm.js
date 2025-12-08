document.addEventListener('DOMContentLoaded', () => {
    // --- ELEMENTOS DO DOM ---
    const divisaoSelect = document.getElementById('divisao-select');
    const anoSelect = document.getElementById('ano-select');
    const alunosComeramInput = document.getElementById('alunos-comeram');
    const comidaFeitaInput = document.getElementById('comida-feita');
    const sobradoDesperdicioInput = document.getElementById('sobrado-desperdicio');
    const enviarBtn = document.getElementById('enviar-btn');
    
    // Elementos do resultado na página
    const resultadoContainer = document.getElementById('resultado-container');
    const valorPercentualSpan = document.getElementById('valor-percentual');
    const valorMediaSpan = document.getElementById('valor-media');
    
    // Elementos do modal
    const mensagemModal = document.getElementById('mensagem-modal');
    const fecharMensagemBtn = document.getElementById('fechar-mensagem-btn');

    // --- FUNÇÕES ---
    function exibirMensagem() {
        mensagemModal.classList.remove('deactive');
    }

    function esconderMensagem() {
        mensagemModal.classList.add('deactive');
    }

    // --- EVENT LISTENER DO BOTÃO ENVIAR ---
    enviarBtn.addEventListener('click', () => {
        // Esconder o resultado anterior antes de calcular um novo
        resultadoContainer.classList.add('deactive');

        // 1. Obter os valores dos campos
        const divisao = divisaoSelect.value;
        const ano = anoSelect.value;
        const totalProduzido = parseFloat(comidaFeitaInput.value);
        const totalDesperdicado = parseFloat(sobradoDesperdicioInput.value);
        const alunos = parseFloat(alunosComeramInput.value);

        // 2. Validação dos dados
        if (!divisao || !ano) {
            alert('Por favor, selecione a Divisão e o Ano.');
            return;
        }
        if (isNaN(totalProduzido) || isNaN(totalDesperdicado) || totalProduzido <= 0) {
            alert('Preencha os campos de comida com valores válidos.');
            return;
        }
        
        // 3. REALIZAR O CÁLCULO
        const percentualDesperdicio = (totalDesperdicado / totalProduzido) * 100;
        let mediaPorAluno = 0;
        if (!isNaN(alunos) && alunos > 0) {
            mediaPorAluno = totalDesperdicado / alunos;
        }

        // 4. EXIBIR O RESULTADO DIRETAMENTE NA PÁGINA
        valorPercentualSpan.textContent = percentualDesperdicio.toFixed(2);
        valorMediaSpan.textContent = mediaPorAluno.toFixed(2);
        resultadoContainer.classList.remove('deactive');
        
        // 5. Exibir o modal de confirmação
        exibirMensagem();

        // 6. Logar o objeto completo para simular envio ao servidor
        const dadosCompletos = {
            divisao: divisao,
            ano: ano,
            totalProduzido: totalProduzido,
            totalDesperdicado: totalDesperdicado,
            percentualDesperdicio: percentualDesperdicio,
            alunosAtendidos: alunos,
            mediaDesperdicioPorAluno: mediaPorAluno
        };
        console.log('Dados para salvar:', dadosCompletos);
    });

    // --- EVENT LISTENER PARA FECHAR O MODAL ---
    fecharMensagemBtn.addEventListener('click', () => {
        esconderMensagem();
    });

    // Fechar o modal ao clicar no fundo escuro
    mensagemModal.addEventListener('click', (event) => {
        if (event.target === mensagemModal) {
            esconderMensagem();
        }
    });
});
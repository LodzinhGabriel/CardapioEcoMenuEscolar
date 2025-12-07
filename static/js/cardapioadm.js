const botao = document.getElementById('cardapioadm-interactive-div');
const input = document.getElementById('arquivo');
const enviar = document.getElementsByClassName('cardapioadm enviar')[0];
const cancelar = document.getElementsByClassName('cardapioadm cancelar')[0];
const esvaziar = document.getElementsByClassName('cardapioadm esvaziar')[0];
const erro = botao.querySelectorAll('#erro')[0];
const nuvem = botao.querySelectorAll('#nuvem')[0];
const arquivos_aceitos = botao.querySelectorAll('#arquivos-aceitos')[0];
const embed = botao.querySelectorAll('#pdf-recebido')[0];
const img = botao.querySelectorAll('#recebido')[0];
const mensagem = document.getElementById('mensagem')
const voltar = document.getElementsByClassName('cardapioadm voltar')[0];

var contemArquivo = false

botao.addEventListener('click', () => {
    if (!contemArquivo) {
        document.getElementById('arquivo').click();
    }
});

input.addEventListener('change', () => {
    const arq = input.files[0];
    if (!arq) return;

    var success = false;
    var e =  null;

    const url = URL.createObjectURL(arq);

    if (arq.type == "application/pdf") {
        embed.classList.remove('deactive');
        embed.src = url;
        success = true
    } else if (arq.type.startsWith("image/")) {
        img.classList.remove('deactive');
        img.src = url;
        success = true
    } else {
         if (erro.classList.contains('deactive')) erro.classList.remove('deactive');
        erro.textContent = "Arquivo solicitado incorreto."
    }

    if (success) {
        contemArquivo = true;
        nuvem.classList.add('deactive');
        erro.classList.add('deactive');
        arquivos_aceitos.classList.add('deactive');
        esvaziar.classList.remove('deactive');
    } else {
        if (nuvem.classList.contains('deactive')) nuvem.classList.remove('deactive');
        if (arquivos_aceitos.classList.contains('deactive')) arquivos_aceitos.classList.remove('deactive');
    }
});

cancelar.addEventListener('click', () => {
    window.location.href = "/nutri";
});

esvaziar.addEventListener('click', () => {
    contemArquivo = false;
    if (nuvem.classList.contains('deactive')) nuvem.classList.remove('deactive');
    if (arquivos_aceitos.classList.contains('deactive')) arquivos_aceitos.classList.remove('deactive');
    if (!embed.classList.contains('deactive')) embed.classList.add('deactive');
    if (!img.classList.contains('deactive')) img.classList.add('deactive');
    esvaziar.classList.add('deactive');
})

enviar.addEventListener('click', () => {
    const arq = input.files[0];

    if (!arq) {
        if (erro.classList.contains('deactive')) erro.classList.remove('deactive');
        erro.textContent = "Nenhum arquivo foi mandado para o envio."
        return;
    }

    if (!arq.type == "application/pdf" && !arq.type.startsWith("image/")) {
        if (erro.classList.contains('deactive')) erro.classList.remove('deactive');
        erro.textContent = "Arquivo solicitado incorreto."
        return;
    }

    const formulario = new FormData();
    formulario.append('arquivo', arq)

    fetch('/cardapio/enviar/upload', {
        method: 'POST',
        body: formulario
    })
    .then(res => res.json())
    .then((data) => {
        mensagem.classList.remove('deactive');
        document.getElementById('texto-sucesso').innerText = data.mensagem || data.erro
        if (data.detalhamento) console.log(data.detalhamento);
    });
});

voltar.addEventListener('click', () => {
    window.location.href = "/nutri";
});
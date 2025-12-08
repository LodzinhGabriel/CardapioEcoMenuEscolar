const botao = document.getElementById('avisoadm-interactive-div');
const input = document.getElementById('arquivo');
const enviar = document.getElementsByClassName('avisoadm enviar')[0];
const esvaziar = document.getElementsByClassName('avisoadm esvaziar')[0];
const cancelar = document.getElementsByClassName('avisoadm cancelar')[0];
const erro = botao.querySelectorAll('#erro')[0];
const mensagem = document.getElementById('mensagem')
const voltar = document.getElementsByClassName('avisoadm voltar')[0];

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
        erro.classList.add('deactive');
    }
});

cancelar.addEventListener('click', () => {
    window.location.href = "/nutri";
});
esvaziar.addEventListener('click', () => {
    contemArquivo = false;
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
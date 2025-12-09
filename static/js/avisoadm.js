const titulo = document.getElementById('titulo')
const botao = document.getElementById('avisoadm-interactive-div');
const input = document.getElementById('imagem');
const texto = document.getElementById('texto')
const enviar = document.getElementsByClassName('avisoadm enviar')[0];
const esvaziar = document.getElementsByClassName('avisoadm esvaziar')[0];
const cancelar = document.getElementsByClassName('avisoadm cancelar')[0];
const erro_geral = document.getElementsByClassName('avisoadm campos')[0].querySelectorAll('#erro')[0];
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

    if (arq.type.startsWith("image/")) {
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

    if (!arq.type.startsWith("image/")) {
        if (erro.classList.contains('deactive')) erro.classList.remove('deactive');
        erro.textContent = "Arquivo solicitado incorreto."
        return;
    }
    
    if (titulo.value == "") {
        if (erro_geral.classList.contains('deactive')) erro_geral.classList.remove('deactive');
        erro_geral.textContent = "Titulo em branco."
        return;
    }

    if (texto.value == "") {
        if (erro_geral.classList.contains('deactive')) erro_geral.classList.remove('deactive');
        erro_geral.textContent = "Texto em branco."
        return;
    }

    if (success) {
        erro.classList.add('deactive');
        erro_geral.classList.add('deactive');
    }

    const formulario = new FormData();
    formulario.append('titulo', titulo.value)
    formulario.append('imagem', arq)
    formulario.append('texto', texto.value)

    fetch('/aviso/enviar/upload', {
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
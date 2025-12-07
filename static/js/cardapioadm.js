const botao = document.getElementById('cardapioadm-interactive-div')
const input = document.getElementById('arquivo')

botao.addEventListener('click', () => {
    document.getElementById('arquivo').click();
});

input.addEventListener('change', () => {
    const arq = input.files[0];
    if (!arquivo) return;

    botao.getElementById('img').classList.add('deactive')
    botao.getElementById('p').classList.add('deactive')

    if (arq.type == "application/pdf") {
        const embed = botao.getElementById('pdf-recebido')
        embed.classList.remove('deactive')
        embed.src = arq
    } else if (arq.type == "image/png" || arq.type == "image/jpg") {
        const img = botao.getElementById('recebido')
        img.classList.remove('deactive')
        img.src = arq
    } else {
        console.log("Arquivo solicitado incorreto.")
    }
});
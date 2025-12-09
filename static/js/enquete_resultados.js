// Obtém os votos enviados pelo Flask (serão inseridos no HTML)
const votos = window.dadosEnquete;

// Contagem de votos por opção
const contagem = {
    "Segunda": 0,
    "Terça": 0,
    "Quarta": 0,
    "Quinta": 0,
    "Sexta": 0,
    "Todos os dias": 0
};

// Conta os votos
votos.forEach(v => {
    if (contagem[v.opcao] !== undefined) {
        contagem[v.opcao]++;
    }
});

const labels = Object.keys(contagem);
const valores = Object.values(contagem);

// ==========================
// GRÁFICO DE BARRAS
// ==========================
new Chart(document.getElementById("graficoBarras"), {
    type: 'bar',
    data: {
        labels: labels,
        datasets: [{
            label: 'Votos',
            data: valores,
            borderWidth: 2
        }]
    },
    options: {
        plugins: { legend: { display: false } },
        scales: { y: { beginAtZero: true } }
    }
});

// ==========================
// GRÁFICO DE PIZZA
// ==========================
new Chart(document.getElementById("graficoPizza"), {
    type: 'pie',
    data: {
        labels: labels,
        datasets: [{
            data: valores
        }]
    }
});

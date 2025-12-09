function toggleMenu() {
    const sidebar = document.querySelector('.sidebar');
    sidebar.classList.toggle('active');
}

function toggleProfile() {
    const profile_container = document.querySelector('.profile-container');
    profile_container.classList.toggle('active');
}

function actionLogout() {
    let profile_container_active = document.querySelector('.profile-container.active');
    if (profile_container_active) window.location.href = "/logout";
}
    
document.addEventListener("click", function(event) {
    const sidebar = document.querySelector('.sidebar');
    const profile_container = document.querySelector('.profile-container')
    const menuButton = document.querySelector('.menu');
    const profileButton = document.querySelector('.profile')
    if (!sidebar.contains(event.target) && !menuButton.contains(event.target)) {
        sidebar.classList.remove('active');
    } 
    if (!profile_container.contains(event.target) && !profileButton.contains(event.target)) {
        profile_container.classList.remove('active');
    }
});



function fecharAviso() {
    const aviso = document.querySelector('.layout.aviso-container');

    fetch('/aviso/leitura', {
        method: 'POST',
    })
    .then(res => res.json())
    .then((data) => {
        console.log(data.mensagem || data.erro)
        aviso.classList.add('deactive');
    });
};
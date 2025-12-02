function toggleMenu() {
    const sidebar = document.querySelector('.sidebar');
    sidebar.classList.toggle('active');
}

function toggleProfile() {
    const profile_container = document.querySelector('.profile-container');
    profile_container.classList.toggle('active');
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
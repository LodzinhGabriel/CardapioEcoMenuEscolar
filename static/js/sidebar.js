var btn = document.querySelector('#sidebar-bttn')
var sidebar = document.querySelector('#sidebar')

console.log(btn)
console.log(sidebar)

btn.addEventListener('click', function() {
    console.log('click')
    sidebar.classList.toggle('active')
})
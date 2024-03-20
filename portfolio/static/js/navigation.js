const hamburger = document.querySelector(".nav__toggle");
const navLinks = document.querySelector(".topnav");

hamburger.addEventListener('click', ()=>{
    navLinks.classList.toggle("open");
});

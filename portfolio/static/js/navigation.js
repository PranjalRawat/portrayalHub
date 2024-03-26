const hamburger = document.querySelector(".nav__toggle");
const navLinks = document.querySelector(".topnav");
const navOptions = document.querySelectorAll(".topnav a")

hamburger.addEventListener('click', ()=>{
    navLinks.classList.toggle("open");
});

// Close navigation links when an option is clicked
navOptions.forEach(option => {
    option.addEventListener('click', () => {
        navLinks.classList.remove("open");
    });
});

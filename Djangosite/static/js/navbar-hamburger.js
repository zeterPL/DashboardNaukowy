const hamburger = document.querySelector(".hamburger");
const hamburgerMenu = document.querySelector(".hamburger-menu");

hamburger.addEventListener("click", (e) => {
    hamburgerMenu.classList.toggle("open");
    hamburgerMenu.classList.toggle("fade");

    hamburger.classList.toggle("open");
})
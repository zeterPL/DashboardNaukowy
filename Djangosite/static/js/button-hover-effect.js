const hoverableButtons = document.querySelectorAll(".hoverable-button");

hoverableButtons.forEach((button) => {
    var hoverEffect = button.querySelector(".button-hover-effect");

    button.addEventListener("mouseenter", (e) => {
        hoverEffect.classList.add("active")
    });

    button.addEventListener("mouseleave", (e) => {
        hoverEffect.classList.remove("active")
    });
})
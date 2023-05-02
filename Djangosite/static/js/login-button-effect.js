const navbarLoginButton = document.querySelector("#navbar-login-button");
const navbarLoginButtonEffect = document.querySelector("#navbar-login-effect");
const navbarLoginLink = document.querySelector("#navbar-login-link");

navbarLoginButton.addEventListener("mouseenter", (e) => {
    navbarLoginButtonEffect.classList.add("active");
    navbarLoginLink.classList.add("active");
});

navbarLoginButton.addEventListener("mouseleave", (e) => {
    navbarLoginButtonEffect.classList.remove("active");
    navbarLoginLink.classList.remove("active");
});

const loginButton = document.querySelector("#login-button-container");
const loginButtonEffect = document.querySelector("#login-button-effect");

loginButton.addEventListener("mouseenter", (e) => {
    loginButtonEffect.classList.add("active");
});

loginButton.addEventListener("mouseleave", (e) => {
    loginButtonEffect.classList.remove("active");
});

const hamburgerLoginButton = document.querySelector("#hamburger-menu-login-button");
const hamburgerLoginButtonEffect = document.querySelector("#hamburger-menu-login-effect");
const hamburgerLoginLink = document.querySelector("#hamburger-login-link");

hamburgerLoginButton.addEventListener("mouseenter", (e) => {
    hamburgerLoginButtonEffect.classList.add("active");
    hamburgerLoginLink.classList.add("active");
});

hamburgerLoginButton.addEventListener("mouseleave", (e) => {
    hamburgerLoginButtonEffect.classList.remove("active");
    hamburgerLoginLink.classList.remove("active");
});
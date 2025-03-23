let cross = document.querySelector("#crossimg");
let menu = document.querySelector("#menuimg");
let getMenu = document.querySelector("#sidemenu");

function closeMenu() {
    getMenu.style.right = "-400px";
}

function openMenu() {
    getMenu.style.right = "0";
}

cross.addEventListener("click", closeMenu);
menu.addEventListener("click", openMenu);

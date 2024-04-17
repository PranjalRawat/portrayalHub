let sidebar = document.querySelector(".sidebar");
let closeBtn = document.querySelector("#btn");
let sidebarNavTitle = document.querySelectorAll(".sidebar .nav-list a");

closeBtn.addEventListener("click", () => {
    sidebar.classList.toggle("open");
    menuBtnChange();
});

for (let [idx, _] of sidebarNavTitle.entries()) {
    sidebarNavTitle[idx].addEventListener("click", () => {
        if (sidebar.classList.contains("open")) {
            sidebar.classList.toggle("open");
            menuBtnChange();
        }
    });
}

function menuBtnChange() {
    if (sidebar.classList.contains("open")) {
        closeBtn.classList.replace("bx-menu", "bx-menu-alt-right");
    } else {
        closeBtn.classList.replace("bx-menu-alt-right", "bx-menu");
    }
}

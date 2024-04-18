let sidebar = document.querySelector(".sidebar");
let homeSection = document.querySelector(".home-section")
let closeBtn = document.querySelector("#btn");
let sidebarNavTitle = document.querySelectorAll(".sidebar .nav-list a");

closeBtn.addEventListener("click", () => {
    toggleSidebarAndHomeSection();
});

for (let [idx, _] of sidebarNavTitle.entries()) {
    const width = window.innerWidth || document.documentElement.clientWidth || document.body.clientWidth;
    sidebarNavTitle[idx].addEventListener("click", () => {
        if (sidebar.classList.contains("open") && width < 986) {
            toggleSidebarAndHomeSection();
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

function toggleSidebarAndHomeSection() {
    sidebar.classList.toggle("open");
    homeSection.classList.toggle("sidebarOpen")
    menuBtnChange();
}

function addClassIfWidthGreaterThanEqual986() {
    const width = window.innerWidth || document.documentElement.clientWidth || document.body.clientWidth;

    if (width >= 986) {
        toggleSidebarAndHomeSection();
    }
}

addClassIfWidthGreaterThanEqual986();

const themeToggle = document.querySelectorAll("#theme-toggle");

for (let [idx, _] of themeToggle.entries()) {
    themeToggle[idx].addEventListener("click", () => {
        document.body.classList.contains("light-theme") ?
            enableDarkMode() :
            enableLightMode();
    });
}

function setCssAttribute(name, value) {
    for (let [idx, _] of themeToggle.entries()) {
        themeToggle[idx].setAttribute(name, value);
    }
}

function enableDarkMode() {
    document.body.classList.remove("light-theme");
    document.body.classList.add("dark-theme");
    setCssAttribute("aria-label", "Light theme");
}

function enableLightMode() {
    document.body.classList.remove("dark-theme");
    document.body.classList.add("light-theme");
    setCssAttribute("aria-label", "Dark theme");
}

function setThemePreference() {
    if (window.matchMedia("(prefers-color-scheme: dark)").matches) {
        enableDarkMode();
        return;
    }
    enableLightMode();
}

document.onload = setThemePreference();

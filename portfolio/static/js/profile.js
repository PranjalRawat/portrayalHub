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

function toggleUpdateProfile(parentClass, editIconId) {
    const update_view = document.querySelector(`.${parentClass} .update_view`);
    const list_view = document.querySelector(`.${parentClass} .list_view`);
    const edit_icon = document.querySelector(`#${editIconId} i`);

    if (update_view.style.display === 'none') {
        update_view.style.display = 'block';
        list_view.style.display = 'none';
        edit_icon.classList.remove('bxs-edit');
        edit_icon.classList.add('bxs-badge-check');
    } else {
        update_view.style.display = 'none';
        list_view.style.display = 'block';
        edit_icon.classList.add('bxs-edit');
        edit_icon.classList.remove('bxs-badge-check');
    }
}

function toggleRemoveItem(parentClass, display) {
    const remove_items = document.querySelectorAll(`.${parentClass} .remove_item`)
    for (let [idx, _] of remove_items.entries()) {
        remove_items[idx].style.display = display
    }
}

function toggleAddItem(parentClass, editIconId) {
    const add_item = document.querySelector(`.${parentClass} .add_item`)
    const edit_icon = document.querySelector(`#${editIconId} i`);

    if (add_item.style.display === 'none') {
        toggleRemoveItem(parentClass, 'block')
        add_item.style.display = 'block';
        add_item.classList.add("list_view");
        edit_icon.classList.remove('bxs-edit');
        edit_icon.classList.add('bxs-badge-check');
    } else {
        add_item.style.display = 'none';
        add_item.classList.remove("list_view");
        toggleRemoveItem(parentClass, 'none')
        edit_icon.classList.add('bxs-edit');
        edit_icon.classList.remove('bxs-badge-check');
    }
}

function toggleAddForm(parentClass) {
    const update_view = document.querySelector(`.${parentClass} .update_view`);

    if (update_view.style.display === 'none') {
        update_view.style.display = 'block';
    } else {
        update_view.style.display = 'none';
    }
}
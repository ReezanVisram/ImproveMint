const openSideMenu = () => {
    const sideMenu = document.getElementById('side-menu');
    sideMenu.classList.add('open');
}

document.getElementById('hamburger').addEventListener('click', openSideMenu);  

const closeSideMenu = () => {
    const sideMenu = document.getElementById('side-menu');
    sideMenu.classList.remove('open');
}

document.getElementById('close-side-menu').addEventListener('click', closeSideMenu);
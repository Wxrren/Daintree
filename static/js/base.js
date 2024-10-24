
function handleHover(elementId, backgroundColor) {
    const element = document.getElementById(elementId);
    element.style.backgroundColor = backgroundColor;
}


document.addEventListener('DOMContentLoaded', () => {
    const links = document.querySelectorAll('.nav-link');

    links.forEach(link => {
        link.addEventListener('mouseover', () => {
            handleHover(link.id, 'white');
        });

        link.addEventListener('mouseout', () => {
            handleHover(link.id, '');
        });
    });
});
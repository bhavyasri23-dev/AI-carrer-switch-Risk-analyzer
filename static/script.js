// Smooth scroll for navbar buttons
document.querySelectorAll('a[href^="#"]').forEach(link => {
    link.addEventListener('click', function (e) {
        e.preventDefault();
        document.querySelector(this.getAttribute('href'))
            .scrollIntoView({ behavior: 'smooth' });
    });
});

// Auto-scroll AFTER Flask reload (important)
window.onload = function () {
    const target = document.body.getAttribute("data-scroll");
    if (target) {
        document.getElementById(target)
            .scrollIntoView({ behavior: "smooth" });
    }
};

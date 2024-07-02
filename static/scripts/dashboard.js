document.addEventListener('DOMContentLoaded', function() {
    const sections = document.querySelectorAll('.section');
    const links = document.querySelectorAll('.sidebar ul li a');

    links.forEach(link => {
        link.addEventListener('click', function(e) {
            const href = this.getAttribute('href');
            if (href.startsWith('#')) {
                e.preventDefault();
                const targetId = href.substring(1);
                sections.forEach(section => {
                    section.style.display = section.id === targetId ? 'block' : 'none';
                });
            } else {
                window.location.href = href;
            }
        });
    });
});


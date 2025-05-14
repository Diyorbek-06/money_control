document.addEventListener('DOMContentLoaded', function() {
    // Navbar linklariga animatsiya
    const navLinks = document.querySelectorAll('.navbar a');
    navLinks.forEach(link => {
        link.addEventListener('mouseover', () => {
            link.style.transform = 'scale(1.1)';
        });
        link.addEventListener('mouseout', () => {
            link.style.transform = 'scale(1)';
        });
    });

    // Dark mode tugmasi
    const darkModeToggle = document.createElement('button');
    darkModeToggle.textContent = 'Dark Mode';
    darkModeToggle.classList.add('dark-mode-btn');
    document.querySelector('.navbar').appendChild(darkModeToggle);

    darkModeToggle.addEventListener('click', () => {
        document.body.classList.toggle('dark-mode');
        darkModeToggle.textContent = document.body.classList.contains('dark-mode') ? 'Light Mode' : 'Dark Mode';
    });
});
document.addEventListener('DOMContentLoaded', function() {
    const heroButtons = document.querySelectorAll('.hero-button');

    heroButtons.forEach(button => {
        button.addEventListener('mouseover', function() {
            heroButtons.forEach(btn => btn.style.animationPlayState = 'paused');
        });

        button.addEventListener('mouseout', function() {
            heroButtons.forEach(btn => btn.style.animationPlayState = 'running');
        });
    });
});
const grayBackground = document.getElementById('grayed-out-background');
const waitlistModal = document.getElementById('waitlist-modal');

function openWaitlist() {
    grayBackground.style.display = 'block';
}

function closeWaitlist() {
    grayBackground.style.display = 'none';
}

document.addEventListener('keydown', function(e) {
    console.log(e.key);
    if (e.key === 'Escape') {
        closeWaitlist();
    }
});

document.getElementById('grayed-out-background').addEventListener('click', function(e) {
    if (e.target === this) {
        closeWaitlist();
    }
});

document.getElementById('waitlist-modal').addEventListener('click', function(e) {
    e.stopPropagation();
});
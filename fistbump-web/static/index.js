const grayBackground = document.getElementById('grayed-out-background');

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
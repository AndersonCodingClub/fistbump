document.addEventListener('DOMContentLoaded', function() {
    const nameInput = document.getElementById('name');
    const emailInput = document.getElementById('email');
    const submitButton = document.querySelector('.modal-submit');

    function updateButtonState() {
        if (nameInput.value.trim().length > 0 && emailInput.value.trim().length > 0) {
            submitButton.classList.add('active');
            submitButton.disabled = false;
        } else {
            submitButton.classList.remove('active');
            submitButton.disabled = true;
        }
    }

    nameInput.addEventListener('input', updateButtonState);
    emailInput.addEventListener('input', updateButtonState);

    updateButtonState();
});

function sendWaitlistEntry() {
    document.getElementById('modal-input-container').style.display = 'none';
    document.getElementById('confirmation-container').style.display = 'block';
}

function openWaitlist() {
    document.getElementById('grayed-out-background').style.display = 'block';
}

function closeWaitlist() {
    document.getElementById('grayed-out-background').style.display = 'none';
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
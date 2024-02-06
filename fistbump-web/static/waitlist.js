async function sendWaitlistEntry() {
    const waitlistName = document.getElementById('name').value;
    const waitlistEmail = document.getElementById('email').value;
    const data = { name: waitlistName, email: waitlistEmail };

    try {
        const response = await fetch('/save-waitlist-entry', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        });

        if (response.ok) {
            document.getElementById('modal-input-container').style.display = 'none';
            document.getElementById('confirmation-container').style.display = 'block';
        } else {
            console.error('Error with fetch call');
        }
    } catch (error) {
        console.error('Network error:', error);
    }
}

function openWaitlist() {
    document.getElementById('grayed-out-background').style.display = 'block';
}

function closeWaitlist() {
    document.getElementById('grayed-out-background').style.display = 'none';
}

document.addEventListener('keydown', function(e) {
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
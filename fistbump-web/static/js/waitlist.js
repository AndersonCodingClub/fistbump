var waitlistName = "";
var waitlistEmail = "";

async function sendVerification() {
    waitlistName = document.getElementById('name').value;
    waitlistEmail = document.getElementById('email').value;
    const data = { name: waitlistName, email: waitlistEmail };
    const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
    const loadingSpinner = document.getElementById('loading-spinner');

    loadingSpinner.style.display = 'block';

    try {
        const response = await fetch('/send-verification', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRF-Token': csrfToken,
            },
            body: JSON.stringify(data)
        });

        if (response.ok) {
            loadingSpinner.style.display = 'none';
            document.getElementById('modal-input-container').style.display = 'none';
            document.getElementById('modal-verification-container').style.display = 'flex';
            document.querySelector('.modal-subtext').innerText = `We've sent a verification code to ${waitlistEmail}. Please check your inbox and enter the code below`;
        } else if (response.status === 400) {
            loadingSpinner.style.display = 'none';
            alert("Email already registered!");
        } else {
            loadingSpinner.style.display = 'none';
            console.error('Error with fetch call');
        }
    } catch (error) {
        loadingSpinner.style.display = 'none';
        console.error('Network error:', error);
    }
}

async function createWaitlistEntry() {
    const verificationCode = document.getElementById('code').value;
    const data = { name: waitlistName, email: waitlistEmail, verificationCode: verificationCode };
    const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');

    try {
        const response = await fetch('/check-code', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRF-Token': csrfToken,
            },
            body: JSON.stringify(data)
        });

        if (response.ok) {
            const responseData = await response.json();
            if (responseData['isValid']) {
                document.getElementById('modal-verification-container').style.display = 'none';
                document.getElementById('confirmation-container').style.display = 'block';
                document.querySelector('.modal-subtext').innerText = `Fistbump is currently in early stage development and are working hard to build \
                                                                      a completely unique social experience. Sign up for the waitlist to get access \
                                                                      as soon as space opens up.`
            } else {
                alert("Incorrect verification code")
            }
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
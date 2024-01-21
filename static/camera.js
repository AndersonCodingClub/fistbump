const video = document.getElementById('video');
const canvas = document.getElementById('canvas');
const captureButton = document.getElementById('captureButton');
const imageElement = document.getElementById('picture');
let stream;
let image;
let imageSavable = false;

// Access the user's camera
navigator.mediaDevices.getUserMedia({ video: true })
    .then((mediaStream) => {
        video.srcObject = mediaStream;
        stream = mediaStream;
    })
    .catch((error) => {
        console.error('Error accessing camera:', error);
    });


video.style.transform = "scaleX(-1)";
canvas.style.transform = "scaleX(-1)";

// Capture button click event
function takePhoto() {
    // Draw the current frame on the canvas
    canvas.getContext('2d').drawImage(video, 0, 0, canvas.width, canvas.height);
    image = canvas.toDataURL();
    imageSavable = true;
}

function saveImage() {
    if (imageSavable) {
        fetch('/capture', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ "dataURL": image })
        });
    }

    setTimeout(() => {window.location.href = '/'}, 1000);
}

function discardImage() {
    canvas.getContext('2d').clearRect(0, 0, canvas. width, canvas. height);
    imageSavable = false;
}
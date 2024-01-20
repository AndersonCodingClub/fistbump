const video = document.getElementById('video');
const canvas = document.getElementById('canvas');
const captureButton = document.getElementById('captureButton');
let stream;
let image;

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
}

function saveImage() {
    fetch('/capture', {
        method: 'POST',
        body: JSON.stringify({"dataURL": image, "time": Date.now()})
    });
}

console.log();
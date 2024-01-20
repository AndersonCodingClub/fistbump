const video = document.getElementById('video');
const canvas = document.getElementById('canvas');
const captureButton = document.getElementById('captureButton');
let stream;

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

// Capture button click event
captureButton.addEventListener('click', () => {
    // Draw the current frame on the canvas
    canvas.getContext('2d').drawImage(video, 0, 0, canvas.width, canvas.height);
    
    // Stop the camera stream
    stream.getTracks().forEach(track => track.stop());
});


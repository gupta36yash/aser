let audioContext;
let recorder;
let isRecording = false;
let recordedBlob;

const recordButton = document.getElementById('recordButton');
const uploadButton = document.getElementById('uploadButton');

recordButton.addEventListener('click', toggleRecording);
uploadButton.addEventListener('click', uploadRecording);

function toggleRecording() {
    if (!audioContext) {
        audioContext = new (window.AudioContext || window.webkitAudioContext)();
    }

    if (isRecording) {
        recorder.stop();
        recorder.exportWAV(blob => {
            recordedBlob = blob;
            uploadButton.disabled = false; // Enable the upload button
        });
        recordButton.textContent = 'Start Recording';
        recordButton.classList.remove('recording');
        isRecording = false;
    } else {
        navigator.mediaDevices.getUserMedia({ audio: true }).then(stream => {
            const input = audioContext.createMediaStreamSource(stream);
            recorder = new Recorder(input, { numChannels: 1 });
            recorder.record();
            recordButton.textContent = 'Stop Recording';
            recordButton.classList.add('recording');
            uploadButton.disabled = true; // Disable the upload button while recording
            isRecording = true;
        }).catch(err => {
            console.error('Error accessing microphone:', err);
        });
    }
}

function uploadRecording() {
    if (recordedBlob) {
        const formData = new FormData();
        formData.append('file', recordedBlob, 'recording.wav');

        fetch('/upload', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            console.log('Success:', data);
            displayJsonData(data);
            uploadButton.classList.add('uploaded');
        })
        .catch(error => console.error('Error:', error));
    }
}

function displayJsonData(data) {
    const jsonContainer = document.getElementById('jsonData');
    jsonContainer.innerHTML = ''; // Clear previous data
    for (const [key, value] of Object.entries(data)) {
        const div = document.createElement('div');
        div.classList.add('key-value');
        div.innerHTML = `<span class="key">${key}:</span> ${value}`;
        jsonContainer.appendChild(div);
    }
}

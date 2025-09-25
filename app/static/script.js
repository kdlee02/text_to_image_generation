function openTab(tabName) {
    document.querySelectorAll('.tab-content').forEach(tab => {
        tab.style.display = 'none';
    });
    document.getElementById(tabName).style.display = 'block';
}

function generateImage() {
    const promptInput = document.getElementById('prompt').value;
    const aspectRatio = document.getElementById('aspect-ratio').value;
    const loadingMessage = document.getElementById('loading-message');
    const generateButton = document.getElementById('generate-button');
    const imageContainer = document.getElementById('image-container');

    if (!promptInput) {
        alert('Please enter a prompt');
        return;
    }

    loadingMessage.style.display = 'block';
    generateButton.style.display = 'none';
    imageContainer.innerHTML = '';

    fetch('/api/generate_image', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ user_input: promptInput, aspect_ratio: aspectRatio })
    })
        .then(response => response.json())
        .then(data => {
            loadingMessage.style.display = 'none';
            generateButton.style.display = 'block';

            if (data.error) {
                alert(data.error);
            } else {
                const img = document.createElement('img');
                img.src = `data:image/png;base64,${data.image}`;
                imageContainer.appendChild(img);
            }
        })
        .catch(error => {
            loadingMessage.style.display = 'none';
            generateButton.style.display = 'block';
            alert('Error generating image. Please try again.');
            console.error('Error:', error);
        });
}

function fetchHistory() {
    const historyLoadingMessage = document.getElementById('history-loading-message');
    const historyButton = document.getElementById('history-button');
    const historyContainer = document.getElementById('history-container');

    historyLoadingMessage.style.display = 'block';
    historyButton.style.display = 'none';
    historyContainer.innerHTML = '';

    fetch('/api/get_images')
        .then(response => response.json())
        .then(data => {
            historyLoadingMessage.style.display = 'none';
            historyButton.style.display = 'block';

            if (data.images.length === 0) {
                historyContainer.innerHTML = '<p>No images found.</p>';
                return;
            }

            data.images.forEach(image => {
                const img = document.createElement('img');
                img.src = `data:image/png;base64,${image.image_base64}`;
                historyContainer.appendChild(img);
            });
        })
        .catch(error => {
            historyLoadingMessage.style.display = 'none';
            historyButton.style.display = 'block';
            alert('Error fetching image history. Please try again.');
            console.error('Error:', error);
        });
}

function openTab(tabName) {
    document.querySelectorAll('.tab-content').forEach(tab => {
        tab.style.display = 'none';
    });
    document.getElementById(tabName).style.display = 'block';
}

function generateImage() {
    const promptInput = document.getElementById('prompt').value;
    const loadingMessage = document.getElementById('loading-message');
    const generateButton = document.getElementById('generate-button');
    const imageContainer = document.getElementById('image-container');

    if (!promptInput) {
        alert('Please enter a prompt');
        return;
    }

    loadingMessage.style.display = 'block';
    generateButton.style.display = 'none';
    // imageContainer.innerHTML = '';

    fetch('/api/generate_image', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ user_input: promptInput})
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
    console.log('fetchHistory function called - NEW VERSION');
    const historyLoadingMessage = document.getElementById('history-loading-message');
    const historyButton = document.getElementById('history-button');
    const historyContainer = document.getElementById('history-container');

    historyLoadingMessage.style.display = 'block';
    historyButton.style.display = 'none';
    historyContainer.innerHTML = '';

    fetch('/api/get_images')
        .then(response => response.json())
        .then(data => {
            console.log('Full API response:', data);
            historyLoadingMessage.style.display = 'none';
            historyButton.style.display = 'block';

            if (!data.images || data.images.length === 0) {
                historyContainer.innerHTML = '<p>No images found. Generate some images first!</p>';
                return;
            }

            console.log('Number of images:', data.images.length);

            data.images.forEach((image, index) => {
                console.log(`Processing image ${index}:`, image);

                const container = document.createElement('div');
                container.style.marginBottom = '20px';
                container.style.border = '2px solid #007bff';
                container.style.padding = '15px';
                container.style.borderRadius = '8px';

                const promptText = document.createElement('p');
                promptText.textContent = `Prompt: ${image.prompt || 'No prompt available'}`;
                promptText.style.fontWeight = 'bold';
                promptText.style.color = '#333';
                promptText.style.marginBottom = '10px';

                const img = document.createElement('img');
                img.src = `data:image/png;base64,${image.image_base64}`;
                img.style.maxWidth = '100%';
                img.style.display = 'block';
                img.style.borderRadius = '4px';

                // Add feedback information
                const feedbackContainer = document.createElement('div');
                feedbackContainer.style.marginTop = '10px';
                feedbackContainer.style.padding = '10px';
                feedbackContainer.style.backgroundColor = '#f8f9fa';
                feedbackContainer.style.borderRadius = '4px';

                if (image.overall_score) {
                    const scoreText = document.createElement('p');
                    scoreText.textContent = `Overall Score: ${image.overall_score}`;
                    scoreText.style.fontWeight = 'bold';
                    scoreText.style.color = '#28a745';
                    scoreText.style.margin = '5px 0';
                    feedbackContainer.appendChild(scoreText);
                }

                if (image.overall_feedback) {
                    const overallFeedbackText = document.createElement('p');
                    overallFeedbackText.textContent = `Overall Feedback: ${image.overall_feedback}`;
                    overallFeedbackText.style.margin = '5px 0';
                    feedbackContainer.appendChild(overallFeedbackText);
                }

                if (image.conflict_description) {
                    const conflictText = document.createElement('p');
                    conflictText.textContent = `Conflicts: ${image.conflict_description}`;
                    conflictText.style.margin = '5px 0';
                    conflictText.style.color = '#dc3545';
                    feedbackContainer.appendChild(conflictText);
                }

                // Add detailed feedback if available
                if (image.subject_feedback) {
                    const subjectText = document.createElement('p');
                    subjectText.textContent = `Subject: ${image.subject_feedback}`;
                    subjectText.style.margin = '5px 0';
                    subjectText.style.fontSize = '0.9em';
                    subjectText.style.color = '#6c757d';
                    feedbackContainer.appendChild(subjectText);
                }

                if (image.art_type_feedback) {
                    const artTypeText = document.createElement('p');
                    artTypeText.textContent = `Art Type: ${image.art_type_feedback}`;
                    artTypeText.style.margin = '5px 0';
                    artTypeText.style.fontSize = '0.9em';
                    artTypeText.style.color = '#6c757d';
                    feedbackContainer.appendChild(artTypeText);
                }

                if (image.art_style_feedback) {
                    const artStyleText = document.createElement('p');
                    artStyleText.textContent = `Art Style: ${image.art_style_feedback}`;
                    artStyleText.style.margin = '5px 0';
                    artStyleText.style.fontSize = '0.9em';
                    artStyleText.style.color = '#6c757d';
                    feedbackContainer.appendChild(artStyleText);
                }

                if (image.art_movement_feedback) {
                    const artMovementText = document.createElement('p');
                    artMovementText.textContent = `Art Movement: ${image.art_movement_feedback}`;
                    artMovementText.style.margin = '5px 0';
                    artMovementText.style.fontSize = '0.9em';
                    artMovementText.style.color = '#6c757d';
                    feedbackContainer.appendChild(artMovementText);
                }

                container.appendChild(promptText);
                container.appendChild(img);
                if (feedbackContainer.children.length > 0) {
                    container.appendChild(feedbackContainer);
                }
                historyContainer.appendChild(container);

                console.log('Added container to historyContainer');
            });
        })
        .catch(error => {
            historyLoadingMessage.style.display = 'none';
            historyButton.style.display = 'block';
            alert('Error fetching image history. Please try again.');
            console.error('Error:', error);
        });
}

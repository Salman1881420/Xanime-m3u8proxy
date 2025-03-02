document.getElementById('form').addEventListener('submit', async function(event) {
    event.preventDefault();

    const apiKey = document.getElementById('api_key').value.trim();
    const fileId = document.getElementById('file_id').value.trim();
    const errorMessage = document.getElementById('error-message');
    const resultDiv = document.getElementById('result');
    const playerContainer = document.getElementById('player-container');
    const videoPlayer = document.getElementById('videoPlayer');
    const videoSource = document.getElementById('videoSource');

    errorMessage.textContent = '';

    if (!apiKey || !fileId) {
        errorMessage.textContent = 'Both API Key and File ID are required!';
        return;
    }

    try {
        // Make the API call to Streamtape
        const response = await fetch(`https://streamtape.com/api/v1/get_video_link?api_key=${apiKey}&file_id=${fileId}`);
        const data = await response.json();

        if (data.success) {
            const directLink = data.result.link;
            resultDiv.textContent = `Direct Video Link: ${directLink}`;
            
            // Show video player
            playerContainer.style.display = 'block';
            videoSource.src = directLink;
            videoPlayer.load();  // Load new video source
            videoPlayer.play();  // Start playing automatically
        } else {
            errorMessage.textContent = 'Error: ' + data.error;
            resultDiv.textContent = '';
        }
    } catch (error) {
        errorMessage.textContent = 'Failed to fetch data. Please check the API and File ID.';
        resultDiv.textContent = '';
    }
});

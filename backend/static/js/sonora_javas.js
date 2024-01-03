
async function getPlaylistImage(playlistId) {
    const imageElement = document.getElementById(`playcover_${playlistId}`);
    if (!imageElement) {
        console.error(`Image element not found for playlist ${playlistId}`);
        return;
    }
    console.log(`Playlist ID: ${playlistId}`);

    fetch(`/getPlaylistImage/${playlistId}`)
        .then(response => response.text())
        .then(data => {
            console.log(`Data from Python for playlist ${playlistId}:\n${data}\n`);
            const coverUrl = data;
            console.log(`Cover URL for playlist ${playlistId}: ${coverUrl}`);
            imageElement.src = coverUrl;
        })
        .catch(error => {
            console.error(`Error for playlist ${playlistId}: ${error}`);
        }
    );
}

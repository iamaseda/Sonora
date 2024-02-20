
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

async function getTrackImage(trackId) {
    const imageElement = document.getElementById(`likedcover_${trackId}`);
    if (!imageElement) {
        console.error(`Image element not found for track ${trackId}`);
        return;
    }
    // console.log(`Track ID: ${trackId}`);

    fetch(`/getTrackImage/${trackId}`)
        .then(response => response.text())
        .then(data => {
            // console.log(`Data from Python for playlist ${trackId}:\n${data}\n`);
            const coverUrl = data;
            console.log(`Cover URL for playlist ${trackId}: ${coverUrl}`);
            imageElement.src = coverUrl;
        })
        .catch(error => {
            console.error(`Error for playlist ${trackId}: ${error}`);
        }
    );
}

function getProfile() {
    fetch(`/home`)
        .then(response => response.json())
        .then(data => {
            const profile = data;
            window.location = '/my-playlists'
        })
        .catch(error => {
            console.error(`Error while retrieving profile data: ${error}`);
        });
}

// function getGenre(id) {
//     // Define the Spotify track query
//     const spotifyTrackQuery = `
//         query GetSpotifyTrack($id: ID!) {
//             spotifyTrack(id: $id) {
//                 id
//                 # Add more fields as needed
//             }
//         }
//     `;

//     // Define the variables for the Spotify track query
//     const spotifyTrackVariables = {
//         id: id, // Replace with the actual track ID
//     };
//     const access_token = process.env.cyanite_access_token;
//     // Make the fetch request
//     fetch("https://api.cyanite.ai/graphql", {
//         method: "POST",
//         body: JSON.stringify({
//             query: spotifyTrackQuery,
//             variables: spotifyTrackVariables,
//         }),
//         headers: {
//             "Content-Type": "application/json",
//             Authorization: "Bearer " + access_token, // Replace with your actual authorization token
//         },
//     })
//     .then((res) => res.json())
//     .then((data) => {
//         // Handle the result data (data will contain the Spotify track information)
//         console.log(data);
//     })
//     .catch((error) => {
//         // Handle errors
//         console.error(error);
//     });
// }
$(document).ready(function() {
    // Add click event listener to the playlist header box
    $('#playlist-sidenav-header-box').click(function() {
        // Get the Spotify Playlist ID from the hidden element
        const spotifyPlaylistId = $(this).find('.spotify-playlist-id').text();
        
        // Redirect to the playlist page using the Spotify Playlist ID
        window.location.href = `/playlist/${spotifyPlaylistId}`;
    });
});

// TODO: while this sidenav persists and functions, rerouting back to the playlist page still hits the Spotify API for the first 50 songs, even if the session's sidenav already has more songs that will overwrite it
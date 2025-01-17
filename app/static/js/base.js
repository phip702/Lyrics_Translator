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

// Show the loading spinner whenever an AJAX request starts
$(document).ajaxStart(function() {
    $('#loading-spinner').show();
});

// Hide the spinner when the AJAX request completes
$(document).ajaxStop(function() {
    $('#loading-spinner').hide();
});

// Alternatively, show the spinner when the page starts loading
$(window).on('beforeunload', function() {
    $('#loading-spinner').show();
});

// Hide the spinner when the page is fully loaded
$(window).on('load', function() {
    $('#loading-spinner').hide();
});

$(window).on('pageshow', function(event) {
    // Hide the spinner when the page is restored
    $('#loading-spinner').hide();
});



document.getElementById('toggle-sidenav').addEventListener('click', function() {
    const sidenav = document.getElementById('playlist-sidenav');
    const body = document.body;
    
    // Toggle collapsed class on body to update the grid layout
    sidenav.classList.toggle('collapsed');
    body.classList.toggle('sidenav-collapsed');
});





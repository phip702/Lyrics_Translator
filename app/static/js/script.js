$(document).ready(function() {

        // BrowserSync script for live reloading
        (function() {
            try {
                var script = document.createElement('script');
                if ('async') {
                    script.async = true;
                }
                script.src = 'http://localhost:3001/browser-sync/browser-sync-client.js?v=3.0.3'.replace("HOST", location.hostname);
                if (document.body) {
                    document.body.appendChild(script);
                } else if (document.head) {
                    document.head.appendChild(script);
                }
            } catch (e) {
                console.error("Browsersync: could not append script tag", e);
            }
        })();




    let rowsCount = $('#tracks-tbody tr').length; 
    let offset = 50;  // Start with an offset of 50 for the first API request

    if (rowsCount % 50 !== 0) { 
        $('#load-more-btn').hide();  // Hide button if not a multiple of 50 because this means all tracks have been loaded
    }
    var spotify_playlist_id = $('#load-more-btn').data('playlist-id');

    // Load more for the body
    $('#load-more-btn').click(function() {
        $.ajax({
            url: `/api/fetch_tracks/${spotify_playlist_id}?offset=${offset}`,
            method: 'GET',
            success: function(response) {
                if (response.length > 0) {
                    // Append the new tracks to the table
                    response.forEach(track => {
                        $('#tracks-tbody').append(`
                            <tr class="track-row">
                                <td><img src="${track.track_image}" alt="Track Image" width="100" height="100"></td>
                                <td>${track.track_artist}</td>
                                <td>${track.track_name}</td>
                                <td class="track-id" style="display: none;">${track.spotify_track_id}</td> <!-- Hidden column for spotify_track_id -->
                            </tr>
                        `);
                    });

                    // Increase the offset by 50 for the next request and update row count
                    offset += 50;
                    let updatedRowCount = $('#tracks-tbody tr').length;
                    if (updatedRowCount % 50 !== 0) {
                        $('#load-more-btn').hide();
                    }
                }
            },

            error: function(error) { // Spotify will never return a blank response, and don't want to implement logic for the case where user has a playlist of a multiple of 50. So will just tell user playlist might be already loaded
                alert('Error fetching tracks. Please try again.\nSpotify playlist might already be fully loaded'); 
            }
        });
    });






    // sidenav always displaying load more button
    // Sidenav Load More functionality
    let sidenavOffset = 50;  // Start with an offset of 50 for the sidenav
    var spotify_playlist_id_sidenav = $('#load-more-sidenav').data('playlist-id');

    // Handle "Load More" for the sidenav
    $('#load-more-sidenav').click(function() {
        $.ajax({
            url: `/api/fetch_tracks/${spotify_playlist_id_sidenav}?offset=${sidenavOffset}`,
            method: 'GET',
            success: function(response) {
                if (response.length > 0) {
                    // Append the new tracks to the sidenav's track list
                    response.forEach(track => {
                        $('#sidenav-tracks').append(`
                                <a class="track-row" href="/track/${track.spotify_track_id}">
                                    <img src="${track.track_image}" alt="Track Image" width="50" height="50">
                                    <div class="track-info">
                                        <span class="track-name">${track.track_name}</span>
                                        <span class="track-artist">${track.track_artist}</span>
                                    </div>
                                </a>
                        `);
                    });

                    // Increase the offset by 50 for the next request
                    sidenavOffset += 50;

                    // Update the rows count and check if it is a multiple of 50
                    sidenavRowsCount = $('#sidenav-tracks li').length;

                    if (sidenavRowsCount % 50 !== 0) {
                        $('#load-more-sidenav').hide();  // Hide button if all tracks are loaded
                    }
                }
            },
            error: function(error) {
                alert('Error fetching tracks. Please try again.');
            }
        });
    });
    
});


// Add event listeners to all table rows
document.querySelectorAll('.track-row').forEach(row => {
    row.addEventListener('click', function() {
    // Get the Spotify track ID from the hidden cell
    const trackId = this.querySelector('.spotify-track-id').innerText;

    // Redirect to the track page using the track ID
    window.location.href = `/track/${trackId}`;
    });
});
$(document).ready(function() {

    //= BrowserSync script for live reloading
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


    //* Load more both
    let rowsCount = $('#tracks-body tr').length; 

    if (rowsCount % 50 !== 0) { 
        $('.load-more').hide();  // Hide button if not a multiple of 50 because this means all tracks have been loaded
    }
    const loadMoreButton = document.querySelector('.load-more');
    const spotifyPlaylistId = loadMoreButton.getAttribute('data-playlist-id');

    // Load more for the body
    $('.load-more').click(function() {
        $.ajax({
            url: `/api/fetch_tracks/${spotifyPlaylistId}?offset=${rowsCount}`,
            method: 'GET',
            success: function(response) {
                if (response.length > 0) {
                    // Append the new tracks to the table or sidenav
                    response.forEach(track => {
                        $('#tracks-body').append(`
                            <tr class="track-row">
                                <td><img src="${track.track_image}" alt="Track Image" width="100" height="100"></td>
                                <td>${track.track_artist}</td>
                                <td>${track.track_name}</td>
                                <td class="track-id" style="display: none;">${track.spotify_track_id}</td>
                            </tr>
                        `);
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

                    // Update the row count and check if the button needs to be hidden
                    let rowsCount = $('#tracks-body').find('tr').length;
                    if (rowsCount % 50 !== 0) {
                        $(".load-more").hide(); // Hide button if all tracks are loaded
                    }
                }
            },
            error: function(error) {
                alert('Error fetching tracks. Please try again.\nSpotify playlist might already be fully loaded');
            }
        });
            
    });




//= Add listeners for every track row to redirect to track URL on user click
document.querySelectorAll('.track-row').forEach(row => {
    row.addEventListener('click', function() {
    // Get the Spotify track ID from the hidden cell
    const trackId = this.querySelector('.spotify-track-id').innerText;

    // Redirect to the track page using the track ID
    window.location.href = `/track/${trackId}`;
    });
});


})
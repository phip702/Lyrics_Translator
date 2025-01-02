$(document).ready(function() {
    let rowsCount = $('#tracks-tbody tr').length; 
    let offset = 50;  // Start with an offset of 50 for the first API request

    if (rowsCount % 50 !== 0) { 
        $('#load-more-btn').hide();  // Hide button if not a multiple of 50 because this means all tracks have been loaded
    }

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

    // reroute to track page when user clicks on a track row
    $(".track-row").on("click", function() {
        var spotify_track_id = $(this).find(".spotify-track-id").text();  // Get the track ID from the hidden column
        console.log("Track ID:", spotify_track_id);
        window.location.href = "/track/" + spotify_track_id; // Redirect to track page
    });
});

$(document).ready(function() {
    let offset = 50;  // Start with an offset of 50 for the first API request

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

                    // Increase the offset by 50 for the next request
                    offset += 50;
                } else {
                    alert('No more tracks available.');
                }
            },
            error: function(error) {
                alert('Error fetching tracks. Please try again.');
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

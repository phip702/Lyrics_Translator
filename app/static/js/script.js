$(document).ready(function() {
    let offset = 50;  // Start with an offset of 50 for the first API request

    // Handle the click event for the "Load More Tracks" button
    $('#load-more-btn').click(function() {
        $.ajax({
            url: `/api/fetch_tracks/${spotify_playlist_id}?offset=${offset}`,
            method: 'GET',
            success: function(response) {
                if (response.length > 0) {
                    // Append the new tracks to the table
                    response.forEach(track => {
                        $('#tracks-tbody').append(`
                            <tr>
                                <td><img src="${track.track_image}" alt="Track Image" width="100" height="100"></td>
                                <td>${track.track_artist}</td>
                                <td>${track.track_name}</td>
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
});

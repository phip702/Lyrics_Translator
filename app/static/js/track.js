$(document).ready(function() {
    // Check if the sidebar data is already in sessionStorage
    var savedSidebar = sessionStorage.getItem('playlistSidebar');

    if (savedSidebar) {
        // If saved data exists, append it to the page
        $('#playlist-sidenav').html(savedSidebar);
    }

    // Function to handle the "Load More" button click
    function handleLoadMoreClick() {
        var playlistId = $(this).data('playlist-id'); // Get the playlist ID from the data attribute
        var offset = $('#tracks-body').find('tr').length; // Get the current count of tracks displayed

        // Send an AJAX request to fetch more tracks based on the playlist ID
        $.ajax({
            url: `/api/fetch_tracks/${playlistId}?offset=${offset}`,
            method: 'GET',
            success: function(response) {
                if (response.length > 0) {
                    // Loop through the response and append new tracks to the table and sidebar
                    response.forEach(function(track) {
                        // Append to the sidebar
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

                    // Save the updated sidebar content to sessionStorage (if needed)
                    saveSidebarToSessionStorage();

                    // Check if there are no more tracks to load, hide the "Load More" button if necessary
                    if (response.length < 50) {  // Adjust based on how many tracks are returned per request
                        $(".load-more").hide();
                        sessionStorage.setItem('loadMoreButtonHidden', 'true'); // Store the visibility state of the button
                    }
                } else {
                    // Optionally handle no more tracks
                    $(".load-more").hide();  // Hide the button if there are no more tracks
                    sessionStorage.setItem('loadMoreButtonHidden', 'true'); // Store the visibility state of the button
                }
            },
            error: function(error) {
                alert('Error fetching tracks. Please try again later.');
            }
        });
    }

    // Listen for the click on the "Load More Tracks" button
    $('.load-more').click(handleLoadMoreClick);

    // Function to save the current sidebar content to sessionStorage
    function saveSidebarToSessionStorage() {
        var sidebarContent = $('#playlist-sidenav').html();
        sessionStorage.setItem('playlistSidebar', sidebarContent);
    }

    // Check if the "Load More" button should be hidden on page load
    var loadMoreButtonHidden = sessionStorage.getItem('loadMoreButtonHidden');
    if (loadMoreButtonHidden === 'true') {
        $(".load-more").hide(); // Ensure the "Load More" button remains hidden
    }
});

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



    //= session saved sidebar
    var savedSidebar = sessionStorage.getItem('playlistSidebar');

    if (savedSidebar) {
        // If saved data exists, append it to the page
        $('#playlist-sidenav').html(savedSidebar);
        // Load the tracks body based on saved sidebar data
        loadTracksFromSidebar(savedSidebar);
    } else {
        // If no saved data, generate the sidebar and save it to sessionStorage
        saveSidebarToSessionStorage();
    }


    //= Load more both
    let rowsCount = $('#sidenav-tracks .track-row').length; 
    console.log(`rowsCount on initialize: ${rowsCount}`);

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
                                <td class="spotify-track-id" style="display: none;">${track.spotify_track_id}</td>
                            </tr>
                        `);
                        $('#sidenav-tracks').append(`
                            <a class="track-row" href="/track/${track.spotify_track_id}">
                                <img src="${track.track_image}" alt="Track Image" width="50" height="50">
                                <div class="track-info">
                                    <span class="track-name">${track.track_name}</span>
                                    <span class="track-artist">${track.track_artist}</span>
                                </div>
                                <span class="spotify-track-id" style="display: none;">${track.spotify_track_id}</span>
                            </a>
                        `);
                    });

                    saveSidebarToSessionStorage();

                    // Update the row count and check if the button needs to be hidden
                    rowsCount = $('#sidenav-tracks .track-row').length;
                    if (rowsCount % 50 !== 0) {
                        $(".load-more").hide(); // Hide button if all tracks are loaded
                    }
                }
                console.log(`rowsCount on load-more end function: ${rowsCount}`);
            },
            error: function(error) {
                console.log(`rowsCount on load-more error: ${rowsCount}`);
                alert('Error fetching tracks. Please try again.\nSpotify playlist might already be fully loaded');
            }
        });
            
    });




//= Add listeners for every track row to redirect to track URL on user click
$(document).on('click', '.track-row', function() {
    // Get the Spotify track ID from the hidden cell
    const trackId = $(this).find('.spotify-track-id').text();

    // Redirect to the track page using the track ID
    window.location.href = `/track/${trackId}`;
});




//= Save to sidebar function
    function saveSidebarToSessionStorage() {
        var sidebarContent = $('#playlist-sidenav').html();  // Get the HTML of the sidebar
        sessionStorage.setItem('playlistSidebar', sidebarContent);  // Save the HTML to sessionStorage
    }




//= If savedsidebar exists then use it to populate the playlist-body
function loadTracksFromSidebar(savedSidebar) {
    // Parse the savedSidebar HTML to find the track links in the sidenav
    const trackLinks = $(savedSidebar).find('.track-row');  // Find all .track-row elements in the saved sidebar

    // Clear the current tracks in the tracks body
    $('#tracks-body').empty();

    // Append each track to the tracks-body using the sidebar information
    trackLinks.each(function() {
        // Extract track information from the link
        const trackId = $(this).find('.spotify-track-id').text(); // Get the spotify track id
        const trackName = $(this).find('.track-name').text();    // Get the track name
        const trackArtist = $(this).find('.track-artist').text(); // Get the track artist
        const trackImage = $(this).find('img').attr('src');      // Get the track image

        // Append the track to the tracks-body with the necessary hidden spotify-track-id
        $('#tracks-body').append(`
            <tr class="track-row">
                <td><img src="${trackImage}" alt="Track Image" width="100" height="100"></td>
                <td>${trackArtist}</td>
                <td>${trackName}</td>
                <td class="spotify-track-id" style="display: none;">${trackId}</td>
            </tr>
        `);
    });
}
    

    



});
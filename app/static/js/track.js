$(document).ready(function() {
    var selectedTrack = localStorage.getItem('selectedTrack');
    
    if (selectedTrack) {
        // Find the track in the sidenav and add an active class or highlight it
        $('#sidenav-tracks .track-row').each(function() {
            if ($(this).find('.spotify-track-id').text() === selectedTrack) {
                $(this).addClass('active');  // You can add a CSS class for active track
            }
        });
    }
});

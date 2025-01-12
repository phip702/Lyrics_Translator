//= Clear saved sidebar whenever user navigates to this main page

$(document).ready(function() {
    // If the user is on the main page (home page with path '/')
    if (window.location.pathname === "/") {
        // Clear the sidebar content from sessionStorage
        sessionStorage.removeItem('playlistSidebar');
    }
});



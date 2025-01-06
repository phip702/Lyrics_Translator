// browser-sync.js
const browserSync = require('browser-sync').create();

browserSync.init({
  proxy: 'http://127.0.0.1:8080',  // Replace with the URL your Flask app is running on
  files: ['app/static/**/*', 'app/templates/*'],  // Watch CSS and template files
  port: 3001,
  open: false,  // Disable automatic browser opening
  notify: false,  // Disable notifications
  ui: {
    port:3003
  }
});

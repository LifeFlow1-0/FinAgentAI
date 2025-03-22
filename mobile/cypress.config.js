const { defineConfig } = require('cypress');

module.exports = defineConfig({
  e2e: {
    baseUrl: 'http://localhost:3000', // Update with your app's development URL
    setupNodeEvents(on, config) {
      // implement node event listeners here
    },
  },
  env: {
    apiUrl: 'http://localhost:8000', // Update with your backend API URL
  },
  viewportWidth: 375,
  viewportHeight: 667, // iPhone 8 dimensions for mobile testing
}); 
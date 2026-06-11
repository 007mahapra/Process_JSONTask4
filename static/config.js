// Configuration for API endpoints
// Dynamically determines the API base URL based on the environment

const API_CONFIG = {
    // Use Railway URL in production, localhost in development
    BASE_URL: window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1'
        ? 'http://localhost:5000'
        : 'https://processjsontask4-production.up.railway.app',
    
    // API endpoints
    ENDPOINTS: {
        RANSOMWARE: '/ransomware',
        LOAD_JSON: '/load_json'
    },
    
    // Helper function to get full URL
    getUrl: function(endpoint) {
        return this.BASE_URL + endpoint;
    }
};

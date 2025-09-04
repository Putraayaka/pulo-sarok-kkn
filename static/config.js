// Konfigurasi API
const API_BASE_URL = 'http://127.0.0.1:8000/pulosarok/api';
const PUBLIC_API_BASE_URL = 'http://127.0.0.1:8000/public/api';
const ADMIN_API_BASE_URL = 'http://127.0.0.1:8000/pulosarok';

// Expose config globally
window.CONFIG = {
    API_BASE_URL,
    PUBLIC_API_BASE_URL,
    ADMIN_API_BASE_URL
};

console.log('Config loaded successfully:', window.CONFIG);
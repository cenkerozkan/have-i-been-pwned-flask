/* Shared Utilities */

// Authentication utilities
function getAuthHeaders() {
    const token = localStorage.getItem('jwt_token');
    return {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
    };
}

function checkAuthentication() {
    const token = localStorage.getItem('jwt_token');
    if (!token) {
        window.location.href = '/api/user/login-page';
        return false;
    }
    return true;
}

function handleAuthError(xhr) {
    if (xhr.status === 401) {
        showAlert('danger', 'Session expired. Please login again.');
        setTimeout(() => {
            window.location.href = '/api/user/login-page';
        }, 2000);
        return true;
    }
    return false;
}

// Alert utilities
function showAlert(type, message) {
    const alert = $('.alert').last();
    alert.removeClass('alert-success alert-danger alert-warning alert-info')
         .addClass(`alert-${type}`)
         .text(message)
         .show();
    
    // Auto-hide success/info messages after 3 seconds
    if (type === 'success' || type === 'info') {
        setTimeout(() => {
            alert.fadeOut();
        }, 3000);
    }
}

// Global logout function
window.logout = function() {
    localStorage.removeItem('jwt_token');
    window.location.href = '/api/user/login-page';
};

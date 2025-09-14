/* Email Management Functions */

function loadEmails() {
    $.ajax({
        url: '/api/email',
        method: 'GET',
        headers: getAuthHeaders(),
        success: function(response) {
            if (response.success) {
                displayEmails(response.data.emails);
            } else {
                showAlert('danger', response.message);
            }
        },
        error: function(xhr) {
            if (!handleAuthError(xhr)) {
                showAlert('danger', 'Failed to load emails. Please try again.');
            }
        }
    });
}

function displayEmails(emails) {
    const emailList = $('#emailList');
    const deleteAllBtn = $('#deleteAllBtn');
    
    if (emails.length === 0) {
        emailList.html('<div class="alert alert-info">No emails added yet. Add your first email above!</div>');
        deleteAllBtn.hide();
        return;
    }

    // Show delete all button when there are emails
    deleteAllBtn.show();

    let emailsHtml = '';
    emails.forEach(email => {
        emailsHtml += `
            <div class="email-item" data-email-id="${email.id}">
                <span class="email-text">${email.email}</span>
                <button type="button" class="btn btn-danger btn-sm" onclick="deleteEmail(${email.id})">
                    Delete
                </button>
            </div>
        `;
    });
    
    emailList.html(emailsHtml);
}

function addEmail() {
    const emailInput = $('#newEmailInput');
    const email = emailInput.val().trim();
    
    if (!email) {
        showAlert('warning', 'Please enter a valid email address.');
        return;
    }

    $.ajax({
        url: '/api/email',
        method: 'POST',
        headers: getAuthHeaders(),
        data: JSON.stringify({ email: email }),
        success: function(response) {
            if (response.success) {
                showAlert('success', response.message);
                emailInput.val(''); // Clear input
                loadEmails(); // Reload email list
            } else {
                showAlert('danger', response.message);
            }
        },
        error: function(xhr) {
            if (!handleAuthError(xhr)) {
                showAlert('danger', 'Failed to add email. Please try again.');
            }
        }
    });
}

// Global function for deleting emails
window.deleteEmail = function(emailId) {
    if (!confirm('Are you sure you want to delete this email?')) {
        return;
    }

    $.ajax({
        url: `/api/email/${emailId}`,
        method: 'DELETE',
        headers: getAuthHeaders(),
        success: function(response) {
            if (response.success) {
                showAlert('success', response.message);
                loadEmails(); // Reload email list
            } else {
                showAlert('danger', response.message);
            }
        },
        error: function(xhr) {
            if (!handleAuthError(xhr)) {
                showAlert('danger', 'Failed to delete email. Please try again.');
            }
        }
    });
};

// Global function for deleting all emails
window.deleteAllEmails = function() {
    if (!confirm('Are you sure you want to delete ALL emails? This action cannot be undone.')) {
        return;
    }

    $.ajax({
        url: '/api/email/all',
        method: 'DELETE',
        headers: getAuthHeaders(),
        success: function(response) {
            if (response.success) {
                showAlert('success', response.message);
                loadEmails(); // Reload email list
            } else {
                showAlert('danger', response.message);
            }
        },
        error: function(xhr) {
            if (!handleAuthError(xhr)) {
                showAlert('danger', 'Failed to delete all emails. Please try again.');
            }
        }
    });
};

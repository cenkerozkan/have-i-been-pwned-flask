/* Breach Management Functions */

function loadBreaches() {
    $.ajax({
        url: '/api/pwned_platforms',
        method: 'GET',
        headers: getAuthHeaders(),
        success: function(response) {
            if (response.success) {
                displayBreaches(response.data.platforms);
            } else {
                showAlert('danger', response.message);
            }
        },
        error: function(xhr) {
            if (!handleAuthError(xhr)) {
                showAlert('danger', 'Failed to load breaches. Please try again.');
            }
        }
    });
}

function displayBreaches(platforms) {
    const breachesContent = $('#breachesContent');
    
    if (platforms.length === 0) {
        breachesContent.html(`
            <div class="alert alert-success">
                <h5>Good news!</h5>
                <p>No security breaches found for your monitored email addresses.</p>
            </div>
        `);
        return;
    }

    // Group breaches by email_id
    const breachesByEmail = {};
    platforms.forEach(breach => {
        if (!breachesByEmail[breach.email_id]) {
            breachesByEmail[breach.email_id] = [];
        }
        breachesByEmail[breach.email_id].push(breach);
    });

    // We need to get email information to display email addresses
    loadEmailsForBreaches(breachesByEmail);
}

function loadEmailsForBreaches(breachesByEmail) {
    $.ajax({
        url: '/api/email',
        method: 'GET',
        headers: getAuthHeaders(),
        success: function(response) {
            if (response.success) {
                displayBreachesGrouped(breachesByEmail, response.data.emails);
            } else {
                $('#breachesContent').html('<div class="alert alert-danger">Failed to load email information</div>');
            }
        },
        error: function(xhr) {
            $('#breachesContent').html('<div class="alert alert-danger">Failed to load email information</div>');
        }
    });
}

function displayBreachesGrouped(breachesByEmail, emails) {
    const breachesContent = $('#breachesContent');
    
    // Create email lookup map
    const emailMap = {};
    emails.forEach(email => {
        emailMap[email.id] = email.email;
    });

    let breachesHtml = '';
    
    Object.keys(breachesByEmail).forEach(emailId => {
        const emailAddress = emailMap[emailId] || `Email ID: ${emailId}`;
        const breaches = breachesByEmail[emailId];
        const breachCount = breaches.length;
        
        breachesHtml += `
            <div class="breach-card">
                <div class="breach-card-header" onclick="toggleBreachCard(${emailId})">
                    <div class="d-flex justify-content-between align-items-center">
                        <div>
                            <strong>${emailAddress}</strong>
                            <span class="text-muted ms-2">(${breachCount} breach${breachCount !== 1 ? 'es' : ''})</span>
                        </div>
                        <i class="bi bi-chevron-down" id="chevron-${emailId}"></i>
                    </div>
                </div>
                <div class="breach-card-body collapse" id="breaches-${emailId}">
        `;
        
        breaches.forEach(breach => {
            const verificationStatus = breach.is_verified ? 'verified' : 'unverified';
            const verificationText = breach.is_verified ? 'Verified' : 'Unverified';
            const breachDate = new Date(breach.breach_date).toLocaleDateString();
            
            breachesHtml += `
                <div class="breach-item">
                    <div class="breach-header">
                        <div class="flex-grow-1">
                            <div class="breach-title">${breach.title || breach.name}</div>
                            <div class="breach-date">Breach Date: ${breachDate}</div>
                        </div>
                        <span class="breach-status breach-${verificationStatus}">${verificationText}</span>
                    </div>
                    
                    ${breach.description ? `<div class="breach-description">${breach.description}</div>` : ''}
                    
                    <div class="data-classes">
                        <strong>Compromised Data:</strong><br>
                        <div class="mt-1">
                            ${breach.data_classes && breach.data_classes.length > 0 
                                ? breach.data_classes.map(dc => `<span class="data-class-tag">${dc}</span>`).join('') 
                                : '<span class="text-muted">No data classification available</span>'
                            }
                        </div>
                    </div>
                </div>
            `;
        });
        
        breachesHtml += `
                </div>
            </div>
        `;
    });
    
    breachesContent.html(breachesHtml);
}

// Global function to toggle breach cards
window.toggleBreachCard = function(emailId) {
    const cardBody = $(`#breaches-${emailId}`);
    const chevron = $(`#chevron-${emailId}`);
    
    cardBody.collapse('toggle');
    
    cardBody.on('shown.bs.collapse', function() {
        chevron.removeClass('bi-chevron-down').addClass('bi-chevron-up');
    });
    
    cardBody.on('hidden.bs.collapse', function() {
        chevron.removeClass('bi-chevron-up').addClass('bi-chevron-down');
    });
};

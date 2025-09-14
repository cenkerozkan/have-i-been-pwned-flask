/* Main Dashboard Logic */

$(document).ready(function() {
    // Check if user is authenticated
    if (!checkAuthentication()) {
        return;
    }

    // Load emails when page loads and when emails tab is shown
    loadEmails();
    
    // Tab event handlers
    $('#emails-tab').on('shown.bs.tab', function() {
        loadEmails();
    });

    $('#breaches-tab').on('shown.bs.tab', function() {
        loadBreaches();
    });

    $('#settings-tab').on('shown.bs.tab', function() {
        loadSchedulerSettings();
    });

    // Form submission handlers
    $('#addEmailForm').on('submit', function(e) {
        e.preventDefault();
        addEmail();
    });

    $('#schedulerSettingsForm').on('submit', function(e) {
        e.preventDefault();
        updateSchedulerSettings();
    });
});

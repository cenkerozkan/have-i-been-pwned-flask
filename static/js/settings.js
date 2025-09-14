/* Scheduler Settings Functions */

function loadSchedulerSettings() {
    loadCurrentSettings();
    loadJobStatus();
}

function loadCurrentSettings() {
    $.ajax({
        url: '/api/scheduler/settings',
        method: 'GET',
        headers: getAuthHeaders(),
        success: function(response) {
            if (response.success) {
                displayCurrentSettings(response.data);
            } else {
                $('#currentScheduleInfo').html('<div class="text-danger">Failed to load settings</div>');
            }
        },
        error: function(xhr) {
            if (!handleAuthError(xhr)) {
                $('#currentScheduleInfo').html('<div class="text-danger">Failed to load settings</div>');
            }
        }
    });
}

function loadJobStatus() {
    $.ajax({
        url: '/api/scheduler/status',
        method: 'GET',
        headers: getAuthHeaders(),
        success: function(response) {
            if (response.success) {
                displayJobStatus(response.data.jobs);
            } else {
                $('#jobStatusInfo').html('<div class="text-danger">Failed to load job status</div>');
            }
        },
        error: function(xhr) {
            if (!handleAuthError(xhr)) {
                $('#jobStatusInfo').html('<div class="text-danger">Failed to load job status</div>');
            }
        }
    });
}

function displayCurrentSettings(settings) {
    const currentScheduleInfo = $('#currentScheduleInfo');
    
    // Populate form with current values
    $('#intervalValue').val(settings.interval_value);
    $('#intervalUnit').val(settings.interval_unit);
    
    currentScheduleInfo.html(`
        <div class="d-flex justify-content-between align-items-center mb-2">
            <span class="fw-bold">Frequency:</span>
            <span class="badge bg-primary">${settings.interval_value} ${settings.interval_unit}</span>
        </div>
        <div class="text-muted small">
            The system checks for new breaches every ${settings.interval_value} ${settings.interval_unit}.
        </div>
    `);
}

function displayJobStatus(jobs) {
    const jobStatusInfo = $('#jobStatusInfo');
    
    if (jobs.length === 0) {
        jobStatusInfo.html('<div class="text-warning">No scheduled jobs found</div>');
        return;
    }

    const job = jobs[0]; // Assuming we're interested in the first job
    const nextRunTime = job.next_run_time ? new Date(job.next_run_time).toLocaleString() : 'Not scheduled';
    
    jobStatusInfo.html(`
        <div class="d-flex justify-content-between align-items-center mb-2">
            <span class="fw-bold">Status:</span>
            <span class="badge bg-success">Active</span>
        </div>
        <div class="d-flex justify-content-between align-items-center mb-2">
            <span class="fw-bold">Job Name:</span>
            <span>${job.name || job.id}</span>
        </div>
        <div class="d-flex justify-content-between align-items-center">
            <span class="fw-bold">Next Run:</span>
            <span class="text-muted small">${nextRunTime}</span>
        </div>
    `);
}

function updateSchedulerSettings() {
    const intervalValue = parseInt($('#intervalValue').val());
    const intervalUnit = $('#intervalUnit').val();

    if (!intervalValue || intervalValue <= 0) {
        showAlert('warning', 'Please enter a valid interval value (positive number).');
        return;
    }

    if (!intervalUnit) {
        showAlert('warning', 'Please select a time unit.');
        return;
    }

    const data = {
        interval_value: intervalValue,
        interval_unit: intervalUnit
    };

    $.ajax({
        url: '/api/scheduler/settings',
        method: 'PUT',
        headers: getAuthHeaders(),
        data: JSON.stringify(data),
        success: function(response) {
            if (response.success) {
                showAlert('success', response.message);
                // Reload the settings to show updated values
                setTimeout(() => {
                    loadSchedulerSettings();
                }, 1000);
            } else {
                showAlert('danger', response.message || 'Failed to update settings');
            }
        },
        error: function(xhr) {
            if (!handleAuthError(xhr)) {
                if (xhr.status === 422) {
                    showAlert('danger', 'Invalid settings format. Please check your input.');
                } else {
                    showAlert('danger', 'Failed to update scheduler settings. Please try again.');
                }
            }
        }
    });
}

// Global function to reload scheduler settings
window.loadSchedulerSettings = function() {
    loadCurrentSettings();
    loadJobStatus();
};

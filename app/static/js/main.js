// Main JavaScript for Telegram Group Manager

// Global functions for Telegram operations
function testConnection() {
    // Show loading state
    showLoading('Testando connessione al bot...');

    fetch('/telegram/test_connection', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        }
    })
    .then(response => {
        hideLoading();
        if (response.ok) {
            showAlert('Connessione al bot Telegram riuscita!', 'success');
        } else {
            showAlert('Errore nella connessione al bot. Verifica il token.', 'error');
        }
    })
    .catch(error => {
        hideLoading();
        console.error('Error testing connection:', error);
        showAlert('Errore nel test di connessione: ' + error.message, 'error');
    });
}

function importUsers() {
    if (!confirm('Vuoi importare gli utenti dal bot Telegram? Questo potrebbe richiedere alcuni secondi.')) {
        return;
    }

    // Show loading state
    showLoading('Importando utenti dal bot...');

    fetch('/telegram/import_users', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        }
    })
    .then(response => {
        hideLoading();
        if (response.ok) {
            showAlert('Utenti importati con successo!', 'success');
            // Reload page to show updated data
            setTimeout(() => {
                window.location.reload();
            }, 1500);
        } else {
            showAlert('Errore durante l\'importazione degli utenti.', 'error');
        }
    })
    .catch(error => {
        hideLoading();
        console.error('Error importing users:', error);
        showAlert('Errore durante l\'importazione: ' + error.message, 'error');
    });
}

function debugUpdates() {
    showLoading('Recuperando updates del bot...');

    fetch('/telegram/debug_updates', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        }
    })
    .then(response => {
        hideLoading();
        if (response.ok) {
            showAlert('Debug completato. Controlla i messaggi di sistema.', 'info');
        } else {
            showAlert('Errore durante il debug.', 'error');
        }
    })
    .catch(error => {
        hideLoading();
        console.error('Error in debug:', error);
        showAlert('Errore nel debug: ' + error.message, 'error');
    });
}

// Utility functions
function showAlert(message, type = 'info') {
    const alertTypes = {
        'success': 'alert-success',
        'error': 'alert-danger',
        'warning': 'alert-warning',
        'info': 'alert-info'
    };

    const alertClass = alertTypes[type] || 'alert-info';

    const alertHTML = `
        <div class="alert ${alertClass} alert-dismissible fade show" role="alert">
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        </div>
    `;

    // Find container for alerts or create one
    let alertContainer = document.querySelector('.alert-container');
    if (!alertContainer) {
        alertContainer = document.createElement('div');
        alertContainer.className = 'alert-container';

        // Insert after navbar
        const navbar = document.querySelector('.navbar');
        if (navbar && navbar.nextSibling) {
            navbar.parentNode.insertBefore(alertContainer, navbar.nextSibling);
        } else {
            document.body.insertBefore(alertContainer, document.body.firstChild);
        }
    }

    alertContainer.innerHTML = alertHTML;

    // Auto-dismiss after 5 seconds
    setTimeout(() => {
        const alert = alertContainer.querySelector('.alert');
        if (alert) {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }
    }, 5000);
}

function showLoading(message = 'Caricamento...') {
    // Remove existing loading if present
    hideLoading();

    const loadingHTML = `
        <div id="loadingOverlay" class="position-fixed top-0 start-0 w-100 h-100 d-flex align-items-center justify-content-center"
             style="background-color: rgba(0,0,0,0.5); z-index: 9999;">
            <div class="card">
                <div class="card-body text-center">
                    <div class="spinner-border text-primary mb-3" role="status">
                        <span class="visually-hidden">Loading...</span>
                    </div>
                    <p class="mb-0">${message}</p>
                </div>
            </div>
        </div>
    `;

    document.body.insertAdjacentHTML('beforeend', loadingHTML);
}

function hideLoading() {
    const overlay = document.getElementById('loadingOverlay');
    if (overlay) {
        overlay.remove();
    }
}

// Form validation utilities
function validateForm(formId) {
    const form = document.getElementById(formId);
    if (!form) return false;

    const requiredFields = form.querySelectorAll('[required]');
    let isValid = true;

    requiredFields.forEach(field => {
        if (!field.value.trim()) {
            field.classList.add('is-invalid');
            isValid = false;
        } else {
            field.classList.remove('is-invalid');
        }
    });

    return isValid;
}

// Auto-save functionality for textareas
function enableAutoSave() {
    const textareas = document.querySelectorAll('.message-textarea');

    textareas.forEach(textarea => {
        const key = `autosave_${textarea.id}`;

        // Load saved content
        const saved = localStorage.getItem(key);
        if (saved) {
            textarea.value = saved;
            // Update character count if function exists
            if (typeof updateCharCount === 'function') {
                updateCharCount(textarea);
            }
        }

        // Save on input
        textarea.addEventListener('input', function() {
            localStorage.setItem(key, this.value);
        });
    });
}

// Clear auto-saved data after successful send
function clearAutoSave() {
    const textareas = document.querySelectorAll('.message-textarea');
    textareas.forEach(textarea => {
        const key = `autosave_${textarea.id}`;
        localStorage.removeItem(key);
    });
}

// Keyboard shortcuts
function setupKeyboardShortcuts() {
    document.addEventListener('keydown', function(e) {
        // Ctrl+S or Cmd+S to save (prevent default and trigger form submit if in message form)
        if ((e.ctrlKey || e.metaKey) && e.key === 's') {
            e.preventDefault();
            const messageForm = document.getElementById('messagesForm');
            if (messageForm) {
                if (confirm('Vuoi inviare tutti i messaggi?')) {
                    messageForm.submit();
                }
            }
        }

        // Escape to close modals
        if (e.key === 'Escape') {
            const openModals = document.querySelectorAll('.modal.show');
            openModals.forEach(modal => {
                const bsModal = bootstrap.Modal.getInstance(modal);
                if (bsModal) {
                    bsModal.hide();
                }
            });
        }
    });
}

// Copy to clipboard functionality
function copyToClipboard(text) {
    if (navigator.clipboard) {
        navigator.clipboard.writeText(text).then(() => {
            showAlert('Copiato negli appunti!', 'success');
        }).catch(err => {
            console.error('Error copying to clipboard:', err);
            fallbackCopyToClipboard(text);
        });
    } else {
        fallbackCopyToClipboard(text);
    }
}

function fallbackCopyToClipboard(text) {
    const textArea = document.createElement('textarea');
    textArea.value = text;
    textArea.style.position = 'fixed';
    textArea.style.left = '-999999px';
    textArea.style.top = '-999999px';
    document.body.appendChild(textArea);
    textArea.focus();
    textArea.select();

    try {
        document.execCommand('copy');
        showAlert('Copiato negli appunti!', 'success');
    } catch (err) {
        console.error('Fallback copy failed:', err);
        showAlert('Impossibile copiare negli appunti', 'error');
    }

    document.body.removeChild(textArea);
}

// Initialize everything when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    // Setup keyboard shortcuts
    setupKeyboardShortcuts();

    // Enable auto-save for message forms
    if (document.querySelector('.message-textarea')) {
        enableAutoSave();
    }

    // Add fade-in animation to cards
    const cards = document.querySelectorAll('.card');
    cards.forEach((card, index) => {
        setTimeout(() => {
            card.classList.add('fade-in');
        }, index * 100);
    });

    // Auto-focus first input in modals
    const modals = document.querySelectorAll('.modal');
    modals.forEach(modal => {
        modal.addEventListener('shown.bs.modal', function() {
            const firstInput = modal.querySelector('input, textarea, select');
            if (firstInput) {
                firstInput.focus();
            }
        });
    });

    // Clear form data when modals are hidden
    modals.forEach(modal => {
        modal.addEventListener('hidden.bs.modal', function() {
            const form = modal.querySelector('form');
            if (form) {
                form.reset();
                // Remove validation classes
                const inputs = form.querySelectorAll('.is-invalid, .is-valid');
                inputs.forEach(input => {
                    input.classList.remove('is-invalid', 'is-valid');
                });
            }
        });
    });
});

// Clean up auto-save data when leaving page
window.addEventListener('beforeunload', function() {
    // Only clear if we're not in a form submission
    const forms = document.querySelectorAll('form');
    let submitting = false;

    forms.forEach(form => {
        if (form.dataset.submitting === 'true') {
            submitting = true;
        }
    });

    if (!submitting) {
        // Don't clear auto-save, let user recover their work
    }
});

// Mark forms as submitting to avoid clearing auto-save
document.addEventListener('submit', function(e) {
    e.target.dataset.submitting = 'true';

    // Clear auto-save for message forms on successful submit
    if (e.target.id === 'messagesForm') {
        setTimeout(() => {
            clearAutoSave();
        }, 1000);
    }
});

// Export functions for global use
window.TelegramGroupManager = {
    testConnection,
    importUsers,
    showAlert,
    showLoading,
    hideLoading,
    validateForm,
    copyToClipboard
};
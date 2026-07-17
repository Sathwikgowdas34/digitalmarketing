/**
 * Main JavaScript Utilities
 */

// Toast notification
function showToast(message, type = 'info', duration = 3000) {
    const toastDiv = document.createElement('div');
    toastDiv.className = `alert alert-${type}`;
    toastDiv.innerHTML = `
        <i class="fas fa-info-circle"></i>
        <span>${message}</span>
    `;
    
    const container = document.querySelector('.toast-container');
    if (container) {
        container.appendChild(toastDiv);
        setTimeout(() => {
            toastDiv.remove();
        }, duration);
    }
}

// Format currency
function formatCurrency(amount, currency = '₹') {
    return currency + amount.toLocaleString('en-IN', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
}

// Debounce function
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Throttle function
function throttle(func, limit) {
    let inThrottle;
    return function(...args) {
        if (!inThrottle) {
            func.apply(this, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    };
}

// Copy to clipboard
function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(() => {
        showToast('Copied to clipboard!', 'success');
    }).catch(() => {
        showToast('Failed to copy', 'danger');
    });
}

// Load image with fallback
function loadImage(img) {
    const src = img.dataset.src;
    if (!src) return;
    
    const image = new Image();
    image.onload = () => {
        img.src = src;
        img.classList.add('fade-in');
    };
    image.onerror = () => {
        img.src = 'https://via.placeholder.com/400x300?text=No+Image';
    };
    image.src = src;
}

// Lazy load images
function lazyLoadImages() {
    const images = document.querySelectorAll('img[data-src]');
    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                loadImage(entry.target);
                observer.unobserve(entry.target);
            }
        });
    });
    images.forEach(img => imageObserver.observe(img));
}

// Fetch with error handling
async function fetchJSON(url, options = {}) {
    try {
        const response = await fetch(url, {
            headers: {
                'Content-Type': 'application/json',
                ...options.headers
            },
            ...options
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        return await response.json();
    } catch (error) {
        console.error('Fetch error:', error);
        showToast('An error occurred', 'danger');
        throw error;
    }
}

// Form validation
function validateForm(form) {
    const formData = new FormData(form);
    const data = Object.fromEntries(formData);
    
    let isValid = true;
    const errors = {};
    
    // Email validation
    if (data.email && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(data.email)) {
        errors.email = 'Invalid email format';
        isValid = false;
    }
    
    // Password validation
    if (data.password && data.password.length < 8) {
        errors.password = 'Password must be at least 8 characters';
        isValid = false;
    }
    
    return { isValid, errors, data };
}

// Format time ago
function formatTimeAgo(date) {
    const seconds = Math.floor((new Date() - date) / 1000);
    const intervals = {
        year: 31536000,
        month: 2592000,
        week: 604800,
        day: 86400,
        hour: 3600,
        minute: 60
    };
    
    for (const [key, value] of Object.entries(intervals)) {
        const interval = Math.floor(seconds / value);
        if (interval >= 1) {
            return interval === 1 ? `1 ${key} ago` : `${interval} ${key}s ago`;
        }
    }
    
    return 'just now';
}

// Parse URL parameters
function getUrlParams() {
    const params = {};
    const searchParams = new URLSearchParams(window.location.search);
    searchParams.forEach((value, key) => {
        params[key] = value;
    });
    return params;
}

// Set URL parameters
function setUrlParams(params) {
    const searchParams = new URLSearchParams(params);
    window.history.pushState({}, '', `${window.location.pathname}?${searchParams}`);
}

// Local Storage helpers
const storage = {
    set: (key, value) => localStorage.setItem(key, JSON.stringify(value)),
    get: (key) => JSON.parse(localStorage.getItem(key)),
    remove: (key) => localStorage.removeItem(key),
    clear: () => localStorage.clear()
};

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    lazyLoadImages();
});

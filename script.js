// Modern OnTime Moving - JavaScript

// API Configuration
const API_BASE_URL = 'http://localhost:5000/api';

// DOM Elements
const bookingForm = document.getElementById('bookingForm');
const formMessage = document.getElementById('formMessage');
const mobileMenuToggle = document.querySelector('.mobile-menu-toggle');
const navLinks = document.querySelector('.nav-links');
const shareModal = document.getElementById('shareModal');
const shareModalImage = document.getElementById('shareModalImage');
const shareModalTitle = document.getElementById('shareModalTitle');
const shareModalDescription = document.getElementById('shareModalDescription');
const shareModalUrl = document.getElementById('shareModalUrl');
const shareFacebook = document.getElementById('shareFacebook');
const shareX = document.getElementById('shareX');
const sharePinterest = document.getElementById('sharePinterest');
const shareEmail = document.getElementById('shareEmail');
const shareCopyButton = document.getElementById('shareCopyButton');
const shareModalClose = document.getElementById('shareModalClose');
const chatLauncher = document.getElementById('chatLauncher');
const chatWidget = document.getElementById('chatWidget');
const chatClose = document.getElementById('chatClose');
const chatMessages = document.getElementById('chatMessages');
const chatForm = document.getElementById('chatForm');
const chatInput = document.getElementById('chatInput');

let activeShareButton = null;
let chatBootstrapped = false;

// Initialize on DOM load
document.addEventListener('DOMContentLoaded', () => {
    initMobileMenu();
    initBookingForm();
    initSmoothScroll();
    initStorySharing();
    initChatbot();
    setMinDate();
});

function initChatbot() {
    if (!chatLauncher || !chatWidget || !chatForm || !chatInput || !chatMessages) {
        return;
    }

    chatLauncher.addEventListener('click', openChat);
    chatClose?.addEventListener('click', closeChat);

    chatForm.addEventListener('submit', async (event) => {
        event.preventDefault();
        const message = chatInput.value.trim();
        if (!message) {
            return;
        }

        appendChatMessage(message, 'user');
        chatInput.value = '';

        const reply = await getChatReply(message);
        appendChatMessage(reply, 'bot');
    });

    chatWidget.querySelectorAll('.chat-quick-action').forEach((button) => {
        button.addEventListener('click', async () => {
            const question = button.getAttribute('data-question');
            if (!question) {
                return;
            }

            openChat();
            appendChatMessage(question, 'user');
            const reply = await getChatReply(question);
            appendChatMessage(reply, 'bot');
        });
    });
}

function openChat() {
    if (!chatWidget || !chatLauncher || !chatInput) {
        return;
    }

    chatWidget.hidden = false;
    chatLauncher.hidden = true;
    chatLauncher.setAttribute('aria-expanded', 'true');
    chatInput.focus();

    if (!chatBootstrapped) {
        appendChatMessage('Hi! I can help with quotes, booking steps, service areas, storage, and moving supplies. What do you need?', 'bot');
        chatBootstrapped = true;
    }
}

function closeChat() {
    if (!chatWidget || !chatLauncher) {
        return;
    }

    chatWidget.hidden = true;
    chatLauncher.hidden = false;
    chatLauncher.setAttribute('aria-expanded', 'false');
}

function appendChatMessage(text, type) {
    if (!chatMessages) {
        return;
    }

    const message = document.createElement('div');
    message.className = `chat-message ${type}`;
    message.textContent = text;
    chatMessages.appendChild(message);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

async function getChatReply(userMessage) {
    try {
        const response = await fetch(`${API_BASE_URL}/chat`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ message: userMessage })
        });

        if (response.ok) {
            const result = await response.json();
            if (result?.reply && typeof result.reply === 'string') {
                return result.reply;
            }
        }
    } catch (error) {
        // Fall back to local replies when chat API is not available.
    }

    return buildLocalChatReply(userMessage);
}

function buildLocalChatReply(input) {
    const message = input.toLowerCase();

    if (message.includes('quote') || message.includes('estimate') || message.includes('price') || message.includes('cost')) {
        return 'You can get a free quote from the Book Now section. Share your move date, pickup and drop-off address, and property size, and our team will confirm details within 24 hours.';
    }

    if (message.includes('book') || message.includes('schedule') || message.includes('reservation')) {
        return 'To book your move, fill out the booking form on this page. We will review your request and contact you quickly to finalize your schedule.';
    }

    if (message.includes('storage') || message.includes('container')) {
        return 'Yes, we offer containerized storage in our secure Port Coquitlam warehouse for both short-term and long-term needs.';
    }

    if (message.includes('area') || message.includes('location') || message.includes('where') || message.includes('service')) {
        return 'We serve the Lower Mainland, BC Interior, Vancouver Island, and surrounding islands.';
    }

    if (message.includes('supply') || message.includes('box') || message.includes('packing')) {
        return 'We provide moving boxes, packing materials, and supplies. We can also assist with customized packing for fragile items.';
    }

    if (message.includes('phone') || message.includes('call') || message.includes('contact')) {
        return 'You can call us directly at (604) 505-0026 or submit the form and we will get back to you.';
    }

    return 'Thanks for your message. I can help with quotes, booking, service areas, storage, and supplies. You can also call us at (604) 505-0026 for immediate help.';
}

// Mobile Menu Toggle
function initMobileMenu() {
    if (mobileMenuToggle) {
        mobileMenuToggle.addEventListener('click', () => {
            navLinks.classList.toggle('active');
        });

        // Close menu when clicking on a link
        navLinks.querySelectorAll('a').forEach(link => {
            link.addEventListener('click', () => {
                navLinks.classList.remove('active');
            });
        });

        // Close menu when clicking outside
        document.addEventListener('click', (e) => {
            if (!mobileMenuToggle.contains(e.target) && !navLinks.contains(e.target)) {
                navLinks.classList.remove('active');
            }
        });
    }
}

// Smooth Scrolling for anchor links
function initSmoothScroll() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                const offsetTop = target.offsetTop - 80; // Account for fixed navbar
                window.scrollTo({
                    top: offsetTop,
                    behavior: 'smooth'
                });
            }
        });
    });
}

// Set minimum date for move_date input to today
function setMinDate() {
    const moveDateInput = document.getElementById('move_date');
    if (moveDateInput) {
        const today = new Date().toISOString().split('T')[0];
        moveDateInput.setAttribute('min', today);
    }
}

function initStorySharing() {
    document.querySelectorAll('.story-share-button').forEach(button => {
        button.addEventListener('click', () => {
            openShareModal(button);
        });
    });

    shareModalClose?.addEventListener('click', closeShareModal);
    shareModal?.querySelectorAll('[data-share-close]').forEach(element => {
        element.addEventListener('click', closeShareModal);
    });
    shareCopyButton?.addEventListener('click', copyShareUrl);

    document.addEventListener('keydown', (event) => {
        if (event.key === 'Escape' && shareModal && !shareModal.hidden) {
            closeShareModal();
        }
    });
}

function openShareModal(button) {
    const storyRow = button.closest('.story-row');
    const storyTitle = storyRow?.querySelector('.story-copy h3')?.textContent?.trim() || 'OnTime Moving';
    const storyText = storyRow?.querySelector('.story-copy p')?.textContent?.trim() || 'See OnTime Moving services.';
    const storyImage = storyRow?.querySelector('.story-image img');

    if (!storyRow || !storyImage) {
        return;
    }

    const imageUrl = new URL(storyImage.getAttribute('src'), window.location.href).href;
    const storyId = storyRow.id || createSlug(storyTitle);
    storyRow.id = storyId;

    const shareUrl = `${window.location.origin}${window.location.pathname}#${storyId}`;
    const shareText = `${storyTitle} - ${storyText}`;

    activeShareButton = button;
    shareModalImage.src = imageUrl;
    shareModalImage.alt = storyImage.alt;
    shareModalTitle.textContent = storyTitle;
    shareModalDescription.textContent = storyText;
    shareModalUrl.value = shareUrl;

    shareFacebook.href = `https://www.facebook.com/sharer/sharer.php?u=${encodeURIComponent(shareUrl)}`;
    shareX.href = `https://twitter.com/intent/tweet?text=${encodeURIComponent(shareText)}&url=${encodeURIComponent(shareUrl)}`;
    sharePinterest.href = `https://pinterest.com/pin/create/button/?url=${encodeURIComponent(shareUrl)}&media=${encodeURIComponent(imageUrl)}&description=${encodeURIComponent(shareText)}`;
    shareEmail.href = `mailto:?subject=${encodeURIComponent(storyTitle)}&body=${encodeURIComponent(`${shareText}\n${shareUrl}`)}`;

    shareModal.hidden = false;
    document.body.style.overflow = 'hidden';
    shareModalClose?.focus();
}

function closeShareModal() {
    if (!shareModal) {
        return;
    }

    shareModal.hidden = true;
    document.body.style.overflow = '';
    shareCopyButton.textContent = 'Copy';
    if (activeShareButton) {
        activeShareButton.focus();
    }
}

async function copyShareUrl() {
    if (!shareModalUrl?.value) {
        return;
    }

    try {
        await navigator.clipboard.writeText(shareModalUrl.value);
        shareCopyButton.textContent = 'Copied';
    } catch (error) {
        console.error('Copy failed:', error);
        shareCopyButton.textContent = 'Unavailable';
    }

    setTimeout(() => {
        if (shareCopyButton) {
            shareCopyButton.textContent = 'Copy';
        }
    }, 1800);
}

function createSlug(text) {
    return text.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/(^-|-$)/g, '');
}

// Booking Form Handling
function initBookingForm() {
    if (bookingForm) {
        bookingForm.addEventListener('submit', handleBookingSubmit);
    }
}

async function handleBookingSubmit(e) {
    e.preventDefault();

    // Get form data
    const formData = new FormData(bookingForm);
    const bookingData = {
        customer_name: formData.get('customer_name'),
        phone: formData.get('phone'),
        email: formData.get('email'),
        moving_from: formData.get('moving_from'),
        moving_to: formData.get('moving_to'),
        move_date: formData.get('move_date'),
        move_size: formData.get('move_size'),
        notes: formData.get('special_instructions') || ''
    };

    // Validate form
    if (!validateBookingForm(bookingData)) {
        return;
    }

    // Submit booking
    await submitBooking(bookingData);
}

function validateBookingForm(data) {
    // Check required fields
    const requiredFields = [
        'customer_name', 
        'phone', 
        'email', 
        'moving_from', 
        'moving_to', 
        'move_date', 
        'move_size'
    ];

    for (const field of requiredFields) {
        if (!data[field] || data[field].trim() === '') {
            showMessage(`Please fill in all required fields.`, 'error');
            return false;
        }
    }

    // Validate email
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(data.email)) {
        showMessage('Please enter a valid email address.', 'error');
        return false;
    }

    // Validate phone (basic check)
    const phoneRegex = /[\d\s\-\(\)]+/;
    if (!phoneRegex.test(data.phone) || data.phone.length < 10) {
        showMessage('Please enter a valid phone number.', 'error');
        return false;
    }

    // Validate date is in the future
    const selectedDate = new Date(data.move_date);
    const today = new Date();
    today.setHours(0, 0, 0, 0);
    if (selectedDate < today) {
        showMessage('Please select a future date for your move.', 'error');
        return false;
    }

    return true;
}

async function submitBooking(bookingData) {
    const submitBtn = bookingForm.querySelector('button[type="submit"]');
    const originalText = submitBtn.textContent;

    try {
        // Disable button and show loading
        submitBtn.disabled = true;
        submitBtn.classList.add('loading');
        submitBtn.textContent = 'Submitting';

        // Send booking to server
        const response = await fetch(`${API_BASE_URL}/booking`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(bookingData)
        });

        const result = await response.json();

        if (response.ok && result.success) {
            showMessage(
                `Booking confirmed! We'll contact you at ${bookingData.phone} within 24 hours.`,
                'success'
            );
            bookingForm.reset();
            
            // Scroll to message
            formMessage.scrollIntoView({ behavior: 'smooth', block: 'center' });

            // Track conversion (if you have analytics)
            if (typeof gtag !== 'undefined') {
                gtag('event', 'booking_submitted', {
                    'event_category': 'engagement',
                    'event_label': bookingData.move_size
                });
            }
        } else {
            showMessage(
                result.error || 'Failed to submit booking. Please try again or call us directly.',
                'error'
            );
        }
    } catch (error) {
        console.error('Booking submission error:', error);
        showMessage(
            'Connection error. Please check your internet and try again, or call us at (604) 505-0026.',
            'error'
        );
    } finally {
        // Re-enable button
        submitBtn.disabled = false;
        submitBtn.classList.remove('loading');
        submitBtn.textContent = originalText;
    }
}

function showMessage(message, type = 'success') {
    formMessage.textContent = message;
    formMessage.className = `form-message ${type}`;
    formMessage.style.display = 'block';

    // Auto-hide error messages after 5 seconds
    if (type === 'error') {
        setTimeout(() => {
            formMessage.style.display = 'none';
        }, 5000);
    }
}

// Phone number formatting
document.getElementById('phone')?.addEventListener('input', function(e) {
    let value = e.target.value.replace(/\D/g, '');
    
    if (value.length > 0) {
        if (value.length <= 3) {
            value = `(${value}`;
        } else if (value.length <= 6) {
            value = `(${value.slice(0, 3)}) ${value.slice(3)}`;
        } else {
            value = `(${value.slice(0, 3)}) ${value.slice(3, 6)}-${value.slice(6, 10)}`;
        }
    }
    
    e.target.value = value;
});

// Intersection Observer for fade-in animations
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('fade-in');
            observer.unobserve(entry.target);
        }
    });
}, observerOptions);

// Observe sections for animation
document.querySelectorAll('section').forEach(section => {
    observer.observe(section);
});

// Form field focus effects
document.querySelectorAll('.form-group input, .form-group select, .form-group textarea').forEach(field => {
    field.addEventListener('focus', function() {
        this.parentElement.classList.add('focused');
    });
    
    field.addEventListener('blur', function() {
        this.parentElement.classList.remove('focused');
    });
});

// Prevent form submission on Enter key (except in textarea)
bookingForm?.addEventListener('keydown', function(e) {
    if (e.key === 'Enter' && e.target.tagName !== 'TEXTAREA') {
        e.preventDefault();
    }
});

// Export functions for testing
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        createSlug,
        validateBookingForm,
        showMessage
    };
}

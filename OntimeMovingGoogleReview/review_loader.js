/**
 * OnTime Moving Review Loader
 * Dynamically loads reviews from the API server
 */

class ReviewLoader {
    constructor(apiBaseUrl = 'http://localhost:5000/api') {
        this.apiBaseUrl = apiBaseUrl;
        this.config = null;
    }

    /**
     * Load configuration from API
     */
    async loadConfig() {
        try {
            const response = await fetch(`${this.apiBaseUrl}/config`);
            const data = await response.json();
            
            if (data.success) {
                this.config = data.config;
                console.log('✅ Configuration loaded');
                return this.config;
            } else {
                console.error('Failed to load config:', data.error);
                return null;
            }
        } catch (error) {
            console.error('Error loading config:', error);
            return null;
        }
    }

    /**
     * Fetch reviews from the API
     */
    async fetchReviews(featured = false, limit = null) {
        try {
            let url = `${this.apiBaseUrl}/reviews`;
            const params = new URLSearchParams();
            
            if (featured) {
                params.append('featured', 'true');
            }
            if (limit) {
                params.append('limit', limit);
            }
            
            if (params.toString()) {
                url += `?${params.toString()}`;
            }
            
            const response = await fetch(url);
            const data = await response.json();
            
            if (data.success) {
                return data.reviews;
            } else {
                console.error('Failed to fetch reviews:', data.error);
                return [];
            }
        } catch (error) {
            console.error('Error fetching reviews:', error);
            return [];
        }
    }

    /**
     * Fetch review statistics
     */
    async fetchStatistics() {
        try {
            const response = await fetch(`${this.apiBaseUrl}/statistics`);
            const data = await response.json();
            
            if (data.success) {
                return data.statistics;
            } else {
                console.error('Failed to fetch statistics:', data.error);
                return null;
            }
        } catch (error) {
            console.error('Error fetching statistics:', error);
            return null;
        }
    }

    /**
     * Generate star HTML
     */
    generateStars(rating) {
        return '★'.repeat(rating) + '☆'.repeat(5 - rating);
    }

    /**
     * Create review card HTML
     */
    createReviewCard(review) {
        return `
            <div class="review-card" data-review-id="${review.id}">
                <div class="review-stars">${this.generateStars(review.rating)}</div>
                <p class="review-text">"${review.review_text}"</p>
                <p class="review-author">— ${review.author_name}</p>
            </div>
        `;
    }

    /**
     * Update featured reviews section
     */
    async updateFeaturedReviews(containerId = 'review-cards-container') {
        const reviews = await this.fetchReviews(true, 3);
        const container = document.getElementById(containerId) || 
                         document.querySelector('.review-cards');
        
        if (!container) {
            console.warn('Review container not found');
            return;
        }

        if (reviews.length === 0) {
            console.warn('No reviews to display');
            return;
        }

        container.innerHTML = reviews.map(review => this.createReviewCard(review)).join('');
        console.log(`✅ Loaded ${reviews.length} featured reviews`);
    }

    /**
     * Update statistics display
     */
    async updateStatistics() {
        const stats = await this.fetchStatistics();
        
        if (!stats) {
            console.warn('No statistics to display');
            return;
        }

        // Update average rating
        const ratingText = document.querySelector('.rating-text');
        if (ratingText) {
            ratingText.textContent = `${stats.average_rating.toFixed(1)} out of 5 stars on Google`;
        }

        // Update total reviews in metrics
        const totalCustomersMetric = document.querySelector('.metric-number');
        if (totalCustomersMetric) {
            // Keep the 11,000+ customers metric, but could show review count elsewhere
            console.log(`📊 Total reviews in database: ${stats.total_reviews}`);
        }

        console.log('✅ Statistics updated', stats);
    }

    /**
     * Update trust metrics from config
     */
    updateTrustMetrics() {
        if (!this.config || !this.config.trustMetrics) {
            console.warn('No trust metrics configuration');
            return;
        }

        const metricsGrid = document.querySelector('.metrics-grid');
        if (!metricsGrid) {
            console.warn('Metrics grid not found');
            return;
        }

        const metrics = this.config.trustMetrics;
        metricsGrid.innerHTML = `
            <div class="metric-item">
                <div class="metric-icon">${metrics.yearsInBusiness.icon}</div>
                <div class="metric-number">${metrics.yearsInBusiness.value}</div>
                <div class="metric-label">${metrics.yearsInBusiness.label}</div>
            </div>
            <div class="metric-item">
                <div class="metric-icon">${metrics.happyCustomers.icon}</div>
                <div class="metric-number">${metrics.happyCustomers.value}</div>
                <div class="metric-label">${metrics.happyCustomers.label}</div>
            </div>
            <div class="metric-item">
                <div class="metric-icon">${metrics.bbbRating.icon}</div>
                <div class="metric-number">${metrics.bbbRating.value}</div>
                <div class="metric-label">${metrics.bbbRating.label}</div>
            </div>
            <div class="metric-item">
                <div class="metric-icon">${metrics.licensed.icon}</div>
                <div class="metric-number">${metrics.licensed.value}</div>
                <div class="metric-label">${metrics.licensed.label}</div>
            </div>
        `;

        console.log('✅ Trust metrics updated');
    }

    /**
     * Update testimonial from a random non-featured review
     */
    async updateTestimonial() {
        const reviews = await this.fetchReviews(false, 10);
        if (reviews.length === 0) {
            console.warn('No reviews for testimonial');
            return;
        }

        // Get a 5-star review that's not already featured
        const testimonialReviews = reviews.filter(r => r.rating === 5 && !r.is_featured);
        const testimonialReview = testimonialReviews[Math.floor(Math.random() * testimonialReviews.length)] || reviews[0];

        const testimonialText = document.querySelector('.testimonial-text');
        const testimonialAuthor = document.querySelector('.testimonial-author');
        const testimonialStars = document.querySelector('.testimonial-stars');

        if (testimonialText && testimonialAuthor) {
            testimonialText.textContent = `"${testimonialReview.review_text}"`;
            testimonialAuthor.textContent = `— ${testimonialReview.author_name}`;
            if (testimonialStars) {
                testimonialStars.textContent = this.generateStars(testimonialReview.rating);
            }
            console.log('✅ Testimonial updated');
        }
    }

    /**
     * Update Google Review links
     */
    updateGoogleReviewLinks() {
        if (!this.config || !this.config.googleReviews) {
            console.warn('No Google Reviews URL in config');
            return;
        }

        const googleUrl = this.config.googleReviews.url;
        const links = document.querySelectorAll('a[href*="google.com/search"]');
        
        links.forEach(link => {
            link.href = googleUrl;
        });

        console.log(`✅ Updated ${links.length} Google review links`);
    }

    /**
     * Initialize and load all dynamic content
     */
    async init() {
        console.log('🔄 Initializing review loader...');
        
        // Load configuration first
        await this.loadConfig();

        // Update all dynamic content
        await Promise.all([
            this.updateFeaturedReviews(),
            this.updateStatistics(),
            this.updateTestimonial()
        ]);

        // Update config-based elements (non-async)
        if (this.config) {
            this.updateTrustMetrics();
            this.updateGoogleReviewLinks();
        }
        
        console.log('✅ Review loader initialized');
    }

    /**
     * Submit a new review
     */
    async submitReview(reviewData) {
        try {
            const response = await fetch(`${this.apiBaseUrl}/reviews`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(reviewData)
            });
            
            const data = await response.json();
            
            if (data.success) {
                console.log('✅ Review submitted successfully');
                return { success: true, reviewId: data.review_id };
            } else {
                console.error('Failed to submit review:', data.error);
                return { success: false, error: data.error };
            }
        } catch (error) {
            console.error('Error submitting review:', error);
            return { success: false, error: error.message };
        }
    }
}

// Auto-initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', async () => {
    console.log('🌐 Page loaded, initializing dynamic content...');
    
    const reviewLoader = new ReviewLoader();
    
    // Try to load dynamic content from API
    try {
        const testResponse = await fetch(reviewLoader.apiBaseUrl + '/statistics');
        
        if (testResponse.ok) {
            console.log('✅ API server is available');
            await reviewLoader.init();
        } else {
            console.log('ℹ️ API server not available, using static fallback content');
        }
    } catch (error) {
        console.log('ℹ️ API server not available, using static fallback content');
        console.log('💡 Start the API server with: python api_server.py');
    }
});

// Make ReviewLoader globally available
window.ReviewLoader = ReviewLoader;

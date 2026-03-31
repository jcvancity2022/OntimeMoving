# OnTime Moving Google Review Landing Page

A modern, conversion-focused landing page with integrated Google Reviews management system using SQLite database.

## 📁 Project Structure

```
OntimeMovingGoogleReview/
├── index.html              # Main landing page
├── review_manager.py       # SQLite database manager for reviews
├── api_server.py           # Flask API server
├── review_loader.js        # JavaScript for dynamic review loading
├── google_reviews_helper.py # Helper for Google Reviews workflow
├── requirements.txt        # Python dependencies
├── reviews.db              # SQLite database (auto-created)
├── setup.py               # Automated setup script
├── start_server.bat       # Windows quick start
├── test_system.py         # Test suite
├── examples.py            # Usage examples
└── README.md              # This file
```

## 🚀 Quick Start

### Option 1: Static Website (No Database)

Simply open `index.html` in your browser. The page includes hardcoded reviews and works without any server.

```bash
# Just open the file
start index.html
```

### Option 2: Dynamic Reviews with Database

**Step 1: Install Python Dependencies**

```bash
pip install -r requirements.txt
```

**Step 2: Initialize Database with Sample Reviews**

```bash
python review_manager.py init
```

**Step 3: Start the API Server**

```bash
python api_server.py
```

The API server will start at `http://localhost:5000`

**Step 4: Open the Landing Page**

Open `index.html` in your browser. To enable dynamic reviews, add this attribute to the `<body>` tag:

```html
<body data-dynamic-reviews="true">
```

## 📊 Database Management

### Using the Review Manager

```python
from review_manager import ReviewManager

# Create manager instance
manager = ReviewManager()

# Add a new review
review_id = manager.add_review(
    author_name="Reg Freebody",
    rating=5,
    review_text="We just completed our second move with 'OnTime Movers' and I'm not sure how much more I could say about how responsible and dependable they are except to say, 'We called them again, because we were sure our belongings would get to our new home safely and 'OnTime.'",
    is_featured=True
)

# Get featured reviews
featured = manager.get_featured_reviews(limit=3)

# Get all reviews
all_reviews = manager.get_all_reviews()

# Get statistics
stats = manager.get_statistics()
print(f"Average Rating: {stats['average_rating']:.1f}")
print(f"Total Reviews: {stats['total_reviews']}")

# Update a review
manager.update_review(review_id, is_featured=False)

# Delete a review
manager.delete_review(review_id)

# Export to JSON
manager.export_to_json('backup.json')

# Import from JSON
manager.import_from_json('backup.json')

# Close connection
manager.close()
```

## ⚙️ Configuration & Dynamic Content

### Configuration File (config.json)

All business information, contact details, trust metrics, and Google Review links are centralized in **config.json**:

```json
{
  "business": {
    "name": "OnTime Moving & Storage",
    "phone": "(604) 505-0026",
    "email": "info@ontime-moving.com",
    "address": "104-1525 Broadway St, Port Coquitlam, BC V3C 6M2"
  },
  "googleReviews": {
    "url": "https://www.google.com/search?..."
  },
  "trustMetrics": {
    "yearsInBusiness": {"value": "22+", "icon": "📅"},
    "happyCustomers": {"value": "11,000+", "icon": "😊"}
  }
}
```

**To update contact info or links:** Simply edit `config.json` - no code changes needed!

### Dynamic Content Loading

The landing page automatically loads content dynamically when the API server is running:

- ✅ **Reviews** - Loads featured reviews from database
- ✅ **Statistics** - Shows real average rating and review count  
- ✅ **Trust Metrics** - Loads from config.json
- ✅ **Testimonials** - Randomly selects from 5-star reviews
- ✅ **Google Links** - Updates all links from config.json

**Fallback:** If API server is not running, static HTML content is displayed (graceful degradation).

**How it works:**
1. Page loads with static fallback content
2. JavaScript (`review_loader.js`) checks if API server is available
3. If available, dynamically replaces content with live data
4. If not available, keeps static content

### Accessing Configuration via API

```javascript
// JavaScript
const response = await fetch('http://localhost:5000/api/config');
const { config } = await response.json();
console.log(config.business.phone); // (604) 505-0026
```

```python
# Python
import requests
response = requests.get('http://localhost:5000/api/config')
config = response.json()['config']
print(config['business']['phone'])  # (604) 505-0026
```

## ✍️ Review Submission & Google Integration

### Web Form Submission

Users can submit reviews directly on your website using the review form at `#submit-review`. The form:

1. **Saves to local database** - All reviews are stored in SQLite
2. **Optionally opens Google Reviews** - If user checks the box, they're directed to post on Google too
3. **Works offline** - If API server isn't running, saves to localStorage

### Managing Review Workflow

Use the Google Reviews Helper to manage reviews:

```python
from google_reviews_helper import GoogleReviewsHelper

helper = GoogleReviewsHelper()

# Show dashboard
helper.display_review_dashboard()

# Get reviews that haven't been posted to Google yet
pending = helper.get_pending_reviews()
print(f"Pending: {len(pending)} reviews")

# Open Google Reviews page to post
helper.open_google_reviews_page()

# After posting to Google, mark as complete
helper.mark_review_posted_to_google(review_id=5)

# Generate a report
helper.generate_review_report('monthly_report.txt')

# Export pending reviews
helper.export_for_google_batch('pending.json')
```

### Command Line Tools

```bash
# Show review dashboard
python google_reviews_helper.py dashboard

# List pending reviews
python google_reviews_helper.py pending

# Generate report
python google_reviews_helper.py report

# Export pending reviews
python google_reviews_helper.py export

# Submit a review interactively
python google_reviews_helper.py submit

# Open Google Reviews page
python google_reviews_helper.py google
```

### Workflow Example

1. **Customer submits review on website**
   - Form at bottom of landing page
   - Review saved to database automatically

2. **Review appears in system**
   ```bash
   python google_reviews_helper.py pending
   ```

3. **Post to Google Reviews**
   - Customer can click "Post to Google Reviews" button
   - Or admin can open Google page and manually post
   ```bash
   python google_reviews_helper.py google
   ```

4. **Mark as posted**
   ```python
   helper.mark_review_posted_to_google(review_id)
   ```

### Command Line Interface

```bash
# Initialize with sample data
python review_manager.py init

# Run interactive demo
python review_manager.py
```

## 🌐 API Endpoints

### Get Reviews

```bash
# Get all reviews
GET http://localhost:5000/api/reviews

# Get featured reviews only
GET http://localhost:5000/api/reviews?featured=true

# Get reviews with limit
GET http://localhost:5000/api/reviews?limit=5

# Get reviews by rating
GET http://localhost:5000/api/reviews?rating=5

# Get specific review
GET http://localhost:5000/api/reviews/1
```

### Add Review

```bash
POST http://localhost:5000/api/reviews
Content-Type: application/json

{
    "author_name": "Jane Smith",
    "rating": 5,
    "review_text": "Amazing moving experience!",
    "review_date": "2026-02-19",
    "is_featured": true
}
```

### Update Review

```bash
PUT http://localhost:5000/api/reviews/1
Content-Type: application/json

{
    "is_featured": false,
    "response_text": "Thank you for your feedback!"
}
```

### Delete Review

```bash
DELETE http://localhost:5000/api/reviews/1
```

### Get Statistics

```bash
GET http://localhost:5000/api/statistics
```

### Search Reviews

```bash
GET http://localhost:5000/api/search?q=excellent
```

### Export All Reviews

```bash
GET http://localhost:5000/api/export
```

## 💻 JavaScript Integration

```javascript
// Create review loader instance
const reviewLoader = new ReviewLoader('http://localhost:5000/api');

// Load and display featured reviews
await reviewLoader.updateFeaturedReviews();

// Update statistics display
await reviewLoader.updateStatistics();

// Submit a new review
const result = await reviewLoader.submitReview({
    author_name: "Mark Richardson",
    rating: 5,
    review_text: "On Time moved my elderly parents. They worked hard for the entire move, I almost can't believe the pace they maintained. Great service and hard workers!"
});

if (result.success) {
    console.log('Review submitted!', result.reviewId);
}
```

## 🔗 Google Reviews Integration

All Google review links in the landing page point to:
```
https://www.google.com/search?q=ontime+moving&...#lrd=0x5485d60c7bda081d:0x31940ea9dfb00809,1,,,,
```

### Current Reviews in Database

The system includes these real Google reviews:

1. **Mark Richardson** (5 stars) - Featured
2. **Thomas Leonard** (5 stars) - Featured
3. **Cindy Lukey** (5 stars) - Featured
4. **Pardees Z** (5 stars)
5. **Reg Freebody** (5 stars)
6. **Xiying Li** (5 stars)

## 📝 Database Schema

### reviews table

| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER | Primary key (auto-increment) |
| author_name | TEXT | Reviewer's name |
| rating | INTEGER | Rating 1-5 stars |
| review_text | TEXT | Review content |
| review_date | TEXT | Date of review |
| response_text | TEXT | Business response |
| response_date | TEXT | Response date |
| is_featured | BOOLEAN | Show on homepage |
| created_at | TIMESTAMP | Record creation time |
| updated_at | TIMESTAMP | Last update time |

### review_stats table

| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER | Fixed at 1 |
| total_reviews | INTEGER | Total review count |
| average_rating | REAL | Average rating |
| five_star_count | INTEGER | Count of 5-star reviews |
| four_star_count | INTEGER | Count of 4-star reviews |
| three_star_count | INTEGER | Count of 3-star reviews |
| two_star_count | INTEGER | Count of 2-star reviews |
| one_star_count | INTEGER | Count of 1-star reviews |
| last_updated | TIMESTAMP | Last stats update |

## 🎨 Features

### Landing Page
- ✅ Sticky navigation header
- ✅ Hero section with dual CTAs
- ✅ Google review showcase (3 featured reviews)
- ✅ Trust metrics (22+ years, 11,000+ customers, A+ BBB)
- ✅ 4-step "How It Works" process
- ✅ Services grid
- ✅ Estimate request form
- ✅ **Review submission form (NEW!)**
- ✅ Testimonial section
- ✅ Contact information with map
- ✅ Full footer with links
- ✅ Fully responsive design

### Review Submission Features ⭐ NEW!
- ✅ On-page review submission form
- ✅ Star rating input (1-5 stars)
- ✅ Automatic save to SQLite database
- ✅ Option to also post to Google Reviews
- ✅ Direct link to Google Reviews page
- ✅ Offline support (saves to localStorage if API unavailable)
- ✅ Beautiful success/error messaging
- ✅ Smooth form validation

### Database Features
- ✅ SQLite database for review storage
- ✅ Full CRUD operations
- ✅ Featured review system
- ✅ Automatic statistics calculation
- ✅ JSON export/import
- ✅ Search functionality
- ✅ Rating filters

### API Features
- ✅ RESTful API endpoints
- ✅ CORS enabled for frontend
- ✅ Error handling
- ✅ Query parameters support
- ✅ JSON responses

## 🛠️ Development

### Testing the API

```bash
# Using curl
curl http://localhost:5000/api/reviews?featured=true

# Using PowerShell
Invoke-WebRequest -Uri "http://localhost:5000/api/reviews?featured=true" | Select-Object -Expand Content
```

### Backup Database

```bash
# Create backup
copy reviews.db reviews_backup.db

# Or use Python
python -c "from review_manager import ReviewManager; ReviewManager().export_to_json('backup.json')"
```

## 📞 Contact Information

- **Address**: 104-1525 Broadway St, Port Coquitlam, BC V3C 6P6
- **Phone**: (604) 505-0026
- **Email**: info@ontime-moving.com
- **Google Reviews**: [View All Reviews](https://www.google.com/search?q=ontime+moving)

## 📄 License

© 2026 OnTime Moving Corp. All rights reserved.

---

**Note**: This system is designed for OnTime Moving (Canada). On Time Moving Inc. in USA is a different company.

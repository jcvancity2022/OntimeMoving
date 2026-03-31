# 🚀 Quick Start Guide - OnTime Moving Review System

## For Website Visitors (Submitting a Review)

### Submit a Review on the Website

1. **Navigate to the review section**
   - Scroll down to "Share Your Experience" section
   - Or click "Write Review" in the navigation menu

2. **Fill out the form**
   - Enter your name
   - Select your star rating (click the stars)
   - Write your review
   - Check the "Also post to Google" box if you want

3. **Submit**
   - Click "Submit Review"
   - Your review is saved to the database
   - If you checked the Google option, you'll see a button to post there too

4. **Post to Google (Optional)**
   - Click "Post to Google Reviews" button
   - You'll be taken to OnTime Moving's Google Business page
   - Click the star rating and write your review there

---

## For Website Administrators

### Update Business Information

Before setup, customize your business details in **config.json**:

```json
{
  "business": {
    "name": "Your Business Name",
    "phone": "(604) 505-0026",
    "email": "info@your-business.com",
    "address": "Your Address"
  },
  "googleReviews": {
    "url": "https://your-google-business-url"
  },
  "trustMetrics": {
    "yearsInBusiness": {"value": "22+"},
    "happyCustomers": {"value": "11,000+"}
  }
}
```

💡 **Tip:** All business info, contact details, trust metrics, and Google links are in this file. Update once, changes appear everywhere!

### First-Time Setup

**Option 1: Automated Setup (Recommended)**
```bash
# Run the setup script
python setup.py
```

**Option 2: Manual Setup**
```bash
# Install dependencies
pip install -r requirements.txt

# Initialize database
python review_manager.py init

# Start the server
python api_server.py
```

**Option 3: Windows One-Click**
```bash
# Just double-click this file
start_server.bat
```

### Daily Operations

#### View Dashboard
```bash
python google_reviews_helper.py dashboard
```

**Output:**
```
📊 OnTime Moving - Review Dashboard
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📝 Total Reviews in System: 12
⭐ Average Rating: 4.8 / 5.0
✨ Featured Reviews: 3
⏳ Pending Google Post: 2
🏆 Five-Star Rate: 91.7%
```

#### Check Pending Reviews
```bash
python google_reviews_helper.py pending
```

This shows reviews that haven't been marked as posted to Google yet.

#### Open Google Reviews Page
```bash
python google_reviews_helper.py google
```

Opens the Google Business review page in your browser.

#### Generate Monthly Report
```bash
python google_reviews_helper.py report
```

Creates a text file with all reviews for your records.

### Managing Reviews via Python

```python
from google_reviews_helper import GoogleReviewsHelper

helper = GoogleReviewsHelper()

# Show dashboard
helper.display_review_dashboard()

# Get pending reviews
pending = helper.get_pending_reviews()
for review in pending:
    print(f"{review['author_name']}: {review['rating']} stars")

# After posting a review to Google, mark it
helper.mark_review_posted_to_google(review_id=5)

# Close when done
helper.close()
```

### Recommended Workflow

1. **Daily** - Check dashboard
   ```bash
   python google_reviews_helper.py dashboard
   ```

2. **When new reviews come in**
   - They're automatically saved to the database
   - Check them with: `python google_reviews_helper.py pending`

3. **Weekly** - Process pending reviews
   - List pending: `python google_reviews_helper.py pending`
   - Note the review details
   - Open Google: `python google_reviews_helper.py google`
   - Encourage customers to post their reviews there

4. **Monthly** - Generate reports
   ```bash
   python google_reviews_helper.py report
   ```

### API Server Management

**Start the server:**
```bash
python api_server.py
```

**Server will run at:**
```
http://localhost:5000
```

**Stop the server:**
- Press `Ctrl+C` in the terminal

### Common Tasks

#### Feature a Review on Homepage
```python
from review_manager import ReviewManager

manager = ReviewManager()
manager.update_review(review_id=5, is_featured=True)
manager.close()
```

#### Add a Business Response
```python
from review_manager import ReviewManager

manager = ReviewManager()
manager.update_review(
    review_id=5, 
    response_text="Thank you for your feedback!",
    response_date="2026-02-19"
)
manager.close()
```

#### Export All Reviews
```python
from review_manager import ReviewManager

manager = ReviewManager()
manager.export_to_json('backup.json')
manager.close()
```

#### Search Reviews
```python
from review_manager import ReviewManager

manager = ReviewManager()
results = manager.search_reviews("professional")
print(f"Found {len(results)} reviews mentioning 'professional'")
manager.close()
```

### Backup & Restore

**Create Backup:**
```bash
# Copy database file
copy reviews.db reviews_backup.db

# Or export to JSON
python -c "from review_manager import ReviewManager; ReviewManager().export_to_json('backup.json')"
```

**Restore from Backup:**
```bash
# Restore database file
copy reviews_backup.db reviews.db

# Or import from JSON
python -c "from review_manager import ReviewManager; m = ReviewManager(); m.import_from_json('backup.json')"
```

### Troubleshooting

**Problem: API server won't start**
- Check if port 5000 is already in use
- Make sure Flask is installed: `pip install flask flask-cors`

**Problem: Reviews not showing on website**
- Check if API server is running
- Add `data-dynamic-reviews="true"` to `<body>` tag in index.html
- Or just use the static reviews (they're hardcoded)

**Problem: Can't submit reviews on website**
- Make sure API server is running: `python api_server.py`
- Check browser console for errors (F12)
- Reviews will be saved to localStorage if API is unavailable

**Problem: Database errors**
- Delete `reviews.db` and reinitialize: `python review_manager.py init`

### Testing

Run the test suite:
```bash
python test_system.py
```

View examples:
```bash
python examples.py
```

---

## Architecture Overview

```
┌─────────────────┐
│   Website Form  │  ← Customer submits review
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   JavaScript    │  ← Sends to API
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   Flask API     │  ← Processes request
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ SQLite Database │  ← Stores review
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Google Reviews  │  ← Customer posts separately
└─────────────────┘
```

## Important Notes

⚠️ **Google Reviews Posting**
- Reviews are saved to your local database first
- Customers must separately post to Google (we can't do this automatically)
- The form provides a direct link to make this easy
- Use the helper tools to track which reviews still need Google posting

✅ **Benefits of This System**
- Backup of all reviews in your database
- Can feature reviews on your website immediately
- Track and manage review workflow
- Generate reports and statistics
- No dependence on Google's API

---

## Support

For issues or questions:
- Check the main [README.md](README.md) for detailed documentation
- Review the [examples.py](examples.py) file for code samples
- Run tests with `python test_system.py`

---

**© 2026 OnTime Moving Corp. All rights reserved.**

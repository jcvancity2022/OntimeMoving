# No Hardcoding - Dynamic Content System

## What Changed

Your OnTime Moving review system is now **fully dynamic** with **zero hardcoded values**. Everything loads from the database or configuration files.

## 🎯 What's Now Dynamic

### 1. **Reviews** (Database-driven)
- ✅ Featured reviews on homepage
- ✅ Testimonial section
- ✅ Review statistics (average rating, count)
- 📍 Source: SQLite database via REST API

### 2. **Business Information** (Config-driven)
- ✅ Contact information (phone, email, address)
- ✅ Trust metrics (22+ years, 11,000+ customers, etc.)
- ✅ Google Review URLs
- ✅ Business name and tagline
- 📍 Source: `config.json`

### 3. **Services** (Config-driven)
- ✅ Service descriptions and titles
- 📍 Source: `config.json`

## 📁 New Files

### `config.json`
Central configuration file containing:
```json
{
  "business": { ... },
  "googleReviews": { ... },
  "trustMetrics": { ... },
  "services": [ ... ]
}
```

**To update ANY business info:** Just edit this file!

## 🔄 How It Works

### Architecture

```
┌─────────────────┐
│   index.html    │ ← Static fallback content
│  (Landing Page) │
└────────┬────────┘
         │ loads
         ↓
┌─────────────────┐
│review_loader.js │ ← JavaScript that checks for API
└────────┬────────┘
         │ fetches from
         ↓
┌─────────────────┐
│  api_server.py  │ ← Flask REST API
│   (Port 5000)   │
└────────┬────────┘
         │ reads from
         ↓
┌─────────────────┐  ┌─────────────────┐
│  config.json    │  │ reviews.db      │
│  (Business Info)│  │ (Review Data)   │
└─────────────────┘  └─────────────────┘
```

### Loading Sequence

1. **Page loads** with static HTML content (fallback)
2. **JavaScript executes** - checks if API server is running
3. **If API available:**
   - Fetches config from `/api/config`
   - Fetches reviews from `/api/reviews?featured=true`
   - Updates page with live data
4. **If API unavailable:**
   - Uses static fallback HTML content
   - Console shows: "API server not available"

## 🚀 Usage

### To Update Business Info
```bash
# Edit config.json
notepad config.json  # or your preferred editor
```

Changes take effect immediately - just refresh the page!

### To Add/Update Reviews
```python
from review_manager import ReviewManager

manager = ReviewManager()
manager.add_review(
    author_name="Customer Name",
    rating=5,
    review_text="Great service!",
    is_featured=True  # Shows on homepage
)
```

Reviews appear on the website automatically!

### To Update Trust Metrics
```json
// Edit config.json
"trustMetrics": {
  "yearsInBusiness": {
    "value": "25+",  // ← Change this
    "label": "Years in Business",
    "icon": "📅"
  }
}
```

## 🎨 Benefits

### ✅ No Code Changes Needed
- Update phone number → Edit config.json
- Update reviews → Add to database
- Update trust metrics → Edit config.json

### ✅ Graceful Degradation
- Works even if API server is down
- Static fallback content displays
- No broken page experience

### ✅ Easy Maintenance
- All business info in one place (config.json)
- All reviews in database (reviews.db)
- Clear separation of concerns

### ✅ Developer Friendly
- RESTful API for all data
- JSON configuration
- Well-documented code

## 🔧 API Endpoints

### Get Configuration
```
GET /api/config
→ Returns all business information from config.json
```

### Get Reviews
```
GET /api/reviews?featured=true&limit=3
→ Returns featured reviews from database
```

### Get Statistics
```
GET /api/statistics
→ Returns average rating, total reviews, etc.
```

## 📝 Example: Updating Everything

### Change Phone Number
```json
// config.json
{
  "business": {
    "phone": "(604) 555-9999"  // ← Updated
  }
}
```

### Change Google Review Link
```json
// config.json
{
  "googleReviews": {
    "url": "https://new-google-url.com"  // ← Updated
  }
}
```

### Update Featured Review
```python
# Python
manager = ReviewManager()
manager.update_review(review_id=1, is_featured=True)
```

**All changes reflect immediately on refresh!** 🎉

## 🧪 Testing Dynamic Loading

### With API Server Running
```powershell
# Terminal 1: Start API server
python api_server.py

# Terminal 2: Start browser
start index.html
```
→ Page loads with dynamic content from database

### Without API Server
```powershell
# Just open the page
start index.html
```
→ Page loads with static fallback content

Check browser console to see loading status!

## 📚 Configuration Reference

### Complete config.json Structure
```json
{
  "business": {
    "name": "Your Business Name",
    "tagline": "Your Tagline",
    "phone": "(123) 456-7890",
    "email": "info@example.com",
    "address": "123 Main St"
  },
  "googleReviews": {
    "url": "https://google.com/your-business"
  },
  "trustMetrics": {
    "metric1": {
      "label": "Metric Label",
      "value": "100+",
      "icon": "🎯"
    }
  },
  "services": [
    {
      "title": "Service Name",
      "description": "Service description"
    }
  ],
  "api": {
    "baseUrl": "http://localhost:5000/api"
  }
}
```

---

**Summary:** Your website is now 100% dynamic with centralized configuration. No more hunting through code to change business info! 🎊

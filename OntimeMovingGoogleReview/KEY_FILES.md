# Key Files Reference - No Hardcoding System

## Configuration & Data Files

### 📝 config.json
**What:** Central configuration for all business information  
**Controls:**
- Contact information (phone, email, address)
- Google Review links
- Trust metrics (years in business, customer count, BBB rating)
- Service descriptions
- API settings

**To update business info:** Edit this file!

### 🗄️ reviews.db
**What:** SQLite database storing all reviews  
**Contains:**
- Customer reviews (name, rating, text, date)
- Review responses
- Featured status
- Statistics (average rating, total count)

**To update reviews:** Use ReviewManager Python class or API

## Code Files

### 🌐 index.html
**What:** Landing page HTML  
**Contains:** Static fallback content that's replaced dynamically  
**Note:** No hardcoded data - everything loads from API/config

### ⚡ review_loader.js
**What:** JavaScript that loads dynamic content  
**Does:**
- Fetches config from API
- Loads reviews from database
- Updates page elements with live data
- Handles graceful fallback if API unavailable

### 🔧 api_server.py
**What:** Flask REST API server  
**Endpoints:**
- `/api/config` - Serves config.json
- `/api/reviews` - Serves reviews from database
- `/api/statistics` - Review stats and analytics
- `/api/reviews` (POST) - Submit new review

### 📊 review_manager.py
**What:** Python class for database operations  
**Methods:**
- `add_review()` - Add new review to database
- `get_featured_reviews()` - Get reviews for homepage
- `get_statistics()` - Calculate review statistics
- `update_review()` - Modify existing reviews

## What to Edit for Common Tasks

### Change Phone Number
📁 **File:** `config.json`  
📝 **Line:** `"phone": "(604) 505-0026"`

### Change Email
📁 **File:** `config.json`  
📝 **Line:** `"email": "info@ontime-moving.com"`

### Change Google Review Link
📁 **File:** `config.json`  
📝 **Line:** `"url": "https://google.com/..."`

### Update "Years in Business"
📁 **File:** `config.json`  
📝 **Line:** `"yearsInBusiness": {"value": "22+"}`

### Update "Happy Customers" Count
📁 **File:** `config.json`  
📝 **Line:** `"happyCustomers": {"value": "11,000+"}`

### Add New Review
📁 **Method:** Python or API  
```python
from review_manager import ReviewManager
manager = ReviewManager()
manager.add_review(
    author_name="Customer Name",
    rating=5,
    review_text="Great service!",
    is_featured=True
)
```

### Feature a Review on Homepage
📁 **Method:** Python or API  
```python
manager.update_review(review_id=1, is_featured=True)
```

### Change Service Descriptions
📁 **File:** `config.json`  
📝 **Section:** `"services": [...]`

## Files You DON'T Need to Edit

### ❌ index.html
- All content loads dynamically
- Only edit for layout/design changes
- Business info comes from config.json

### ❌ Python Files (Unless Adding Features)
- api_server.py - Already serves all endpoints
- review_manager.py - Complete database operations
- google_reviews_helper.py - Full workflow tools

### ❌ JavaScript (Unless Adding Features)
- review_loader.js - Handles all dynamic loading
- Auto-initializes on page load

## File Structure

```
OntimeMovingGoogleReview/
│
├── config.json             ← EDIT THIS for business info
├── reviews.db              ← Database (managed by Python)
│
├── index.html              ← Landing page (rarely edit)
├── review_loader.js        ← Dynamic loader (rarely edit)
│
├── api_server.py           ← REST API server
├── review_manager.py       ← Database manager
├── google_reviews_helper.py ← Workflow tools
│
├── setup.py               ← First-time setup
├── test_system.py         ← Testing
├── examples.py            ← Usage examples
├── demo_workflow.py       ← Interactive demo
│
├── requirements.txt       ← Python dependencies
├── README.md             ← Full documentation
├── QUICKSTART.md         ← Quick start guide
├── DYNAMIC_CONTENT.md    ← This system explained
└── KEY_FILES.md          ← This file!
```

## Quick Reference Card

| **Task** | **File** | **Method** |
|----------|----------|------------|
| Change phone/email | `config.json` | Edit directly |
| Update trust metrics | `config.json` | Edit directly |
| Change Google link | `config.json` | Edit directly |
| Add review | `review_manager.py` | Python code |
| Feature review | `review_manager.py` | Python code |
| View all reviews | API or Python | `manager.get_all_reviews()` |
| See statistics | API or Python | `manager.get_statistics()` |

## The Golden Rule

### ✅ DO Edit:
- **config.json** - For ANY business information
- **Use Python/API** - For review operations

### ❌ DON'T Edit:
- index.html (unless changing layout)
- Python files (unless adding features)
- JavaScript files (unless adding features)

---

**Remember:** Everything is now centralized. One config file, one database, automatic updates! 🎉

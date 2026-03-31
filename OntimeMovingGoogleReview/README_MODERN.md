# OnTime Moving - Modern Website Design

A clean, mobile-first booking system designed for younger users with a modern aesthetic.

## 🎨 Design Features

- **Modern UI**: Clean design with green accents, large spacing, and rounded buttons
- **Mobile-First**: Fully responsive layout that works on all devices
- **Fast & Simple**: Easy-to-use booking form on the homepage
- **Professional**: Hero section with stats and clear call-to-action

## 📁 File Structure

```
OnTime Moving/
├── index_modern.html     # Modern homepage with hero & booking form
├── styles.css           # Modern CSS with design system
├── script.js            # JavaScript for form handling & interactions
├── database.py          # SQLite database functions
├── server.py            # Flask API server
├── ontime_moving.db     # SQLite database
└── README_MODERN.md     # This file
```

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install flask flask-cors
```

### 2. Initialize Database

```bash
python database.py init
```

This creates the database and adds 3 test bookings.

### 3. Start the Server

```bash
python server.py
```

### 4. Access the Website

Open your browser to: **http://localhost:5000**

## 🎯 Features

### Homepage (index_modern.html)
- **Hero Section**: Eye-catching headline with "Get a Quote" button
- **Stats**: Display key metrics (500+ customers, 5.0 rating)
- **Services**: 4 service cards with icons
- **How It Works**: 3-step process explanation
- **Booking Form**: Inline form on homepage for quick bookings
- **Reviews**: Social proof with customer testimonials
- **Footer**: Contact info and service areas

### Booking Form Fields
- Customer Name
- Phone Number (auto-formatted)
- Email Address
- Moving From (address)
- Moving To (address)
- Move Date (date picker with future dates only)
- Property Size (dropdown selection)
- Special Instructions (optional notes)

### Design System (styles.css)
- **Color Palette**:
  - Primary Green: `#10b981`
  - Dark Gray: `#1f2937`
  - Light Background: `#f9fafb`
  - White: `#ffffff`
  
- **Typography**:
  - System fonts for fast loading
  - Clear hierarchy with appropriate sizing
  - Readable line-heights

- **Spacing**:
  - Consistent spacing scale (0.5rem to 6rem)
  - Large spacing for modern feel
  - Breathing room around elements

- **Components**:
  - Rounded buttons (12px radius)
  - Card-based layouts
  - Smooth hover effects
  - Mobile-responsive grid

### JavaScript Features (script.js)
- Mobile menu toggle
- Smooth scrolling navigation
- Form validation
- Phone number formatting
- Success/error messages
- Loading states
- Fade-in animations
- API integration

## 🔌 API Endpoints

### Create Booking
```http
POST /api/booking
Content-Type: application/json

{
  "customer_name": "John Doe",
  "phone": "(604) 555-1234",
  "email": "john@example.com",
  "moving_from": "123 Main St, Vancouver",
  "moving_to": "456 Oak Ave, Burnaby",
  "move_date": "2026-03-20",
  "move_size": "2-bedroom",
  "notes": "Piano needs special care"
}
```

### Get All Bookings
```http
GET /api/bookings
GET /api/bookings?status=pending
GET /api/bookings?limit=10
GET /api/bookings?search=John
```

### Get Specific Booking
```http
GET /api/booking/1
```

### Update Booking Status
```http
PATCH /api/booking/1/status
Content-Type: application/json

{
  "status": "confirmed"
}
```

### Delete Booking
```http
DELETE /api/booking/1
```

### Get Upcoming Bookings
```http
GET /api/bookings/upcoming?limit=5
```

### Get Statistics
```http
GET /api/statistics
```

### Health Check
```http
GET /api/health
```

## 💾 Database Schema

```sql
CREATE TABLE bookings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_name TEXT NOT NULL,
    phone TEXT NOT NULL,
    email TEXT NOT NULL,
    moving_from TEXT NOT NULL,
    moving_to TEXT NOT NULL,
    move_date TEXT NOT NULL,
    move_size TEXT,
    notes TEXT,
    status TEXT DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Status Values
- `pending` - New booking, not yet confirmed
- `confirmed` - Booking confirmed by team
- `completed` - Move completed successfully
- `cancelled` - Booking cancelled

## 🎨 Color Usage Guide

### Green Accents (`#10b981`)
- Primary buttons
- Logo text
- Important stats and numbers
- Links on hover
- Success messages

### Dark Gray (`#1f2937`)
- Main text content
- Headings
- Footer background
- Navigation text

### Light Gray (`#f9fafb`)
- Section backgrounds
- Card backgrounds
- Input backgrounds

### White (`#ffffff`)
- Main background
- Button text
- Cards on light backgrounds

## 📱 Responsive Breakpoints

- **Desktop**: 1200px+ (full layout)
- **Tablet**: 768px - 1199px (2-column grid)
- **Mobile**: < 768px (single column, hamburger menu)

## 🧪 Testing the System

### Test Database Functions
```bash
python database.py
```

### Test Booking Creation
```python
from database import Database

db = Database()
booking_id = db.insert_booking(
    customer_name="Test User",
    phone="(604) 555-1234",
    email="test@example.com",
    moving_from="123 Test St",
    moving_to="456 Test Ave",
    move_date="2026-04-01",
    move_size="2-bedroom",
    notes="Test booking"
)
print(f"Created booking: {booking_id}")
db.close()
```

### Test API with cURL
```bash
# Create booking
curl -X POST http://localhost:5000/api/booking \
  -H "Content-Type: application/json" \
  -d '{
    "customer_name": "Jane Doe",
    "phone": "(604) 555-5678",
    "email": "jane@example.com",
    "moving_from": "789 Test Rd",
    "moving_to": "101 Test Blvd",
    "move_date": "2026-03-25",
    "move_size": "1-bedroom",
    "notes": "Test via API"
  }'

# Get all bookings
curl http://localhost:5000/api/bookings
```

## 🔒 Security Notes

**For Production**, implement:
- HTTPS/SSL certificates
- Rate limiting on API endpoints
- Input sanitization
- CSRF protection
- API authentication
- Database backups
- Environment variables for sensitive data

## 🚀 Deployment

### Local Development
```bash
python server.py
```
Runs on http://localhost:5000 with debug mode enabled.

### Production
1. Set `debug=False` in server.py
2. Use a production WSGI server (Gunicorn, uWSGI)
3. Configure reverse proxy (Nginx, Apache)
4. Enable HTTPS
5. Set up monitoring and logging

## 📊 Performance

- **Page Load**: Fast with minimal CSS/JS
- **No External Dependencies**: System fonts only
- **Optimized Images**: Use modern formats (WebP)
- **Mobile-First**: Optimized for mobile networks

## 🎯 Target Audience

- **Age**: 25-40 years old
- **Tech-Savvy**: Comfortable with online booking
- **Mobile Users**: Primarily access via smartphones
- **Value**: Appreciate clean, simple interfaces

## ✨ Modern Design Principles

1. **Simplicity**: Remove unnecessary elements
2. **Whitespace**: Let content breathe
3. **Typography**: Clear hierarchy and readability
4. **Color**: Limited palette with purpose
5. **Mobile-First**: Design for smallest screen first
6. **Feedback**: Clear success/error states
7. **Speed**: Fast loading and interactions

## 🔄 Future Enhancements

Potential additions:
- [ ] Email notifications on booking
- [ ] SMS confirmations
- [ ] Real-time availability calendar
- [ ] Instant pricing calculator
- [ ] Customer portal for tracking
- [ ] Payment integration
- [ ] Photo upload for inventory
- [ ] Live chat support
- [ ] Progressive Web App (PWA)
- [ ] Dark mode option

## 📞 Support

- **Website**: http://localhost:5000
- **API**: http://localhost:5000/api
- **Phone**: (604) 505-0026
- **Email**: info@ontime-moving.com

## 📝 License

© 2026 OnTime Moving. All rights reserved.

---

## 🎉 Getting Started Summary

1. Install: `pip install flask flask-cors`
2. Initialize: `python database.py init`
3. Start: `python server.py`
4. Visit: http://localhost:5000
5. Book a move and see it in action!

**Enjoy your modern booking system! 🚚💚**

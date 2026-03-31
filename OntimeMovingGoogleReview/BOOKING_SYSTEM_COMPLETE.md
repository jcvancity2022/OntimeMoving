# OnTime Moving - Enhanced Booking System

## 🎉 Complete System Overview

A full-featured booking management system for OnTime Moving with SQLite database, REST API, web forms, and admin dashboard.

## 📋 Features Implemented

### ✅ Database (SQLite)
- **Enhanced Schema** with 13 fields:
  - id (primary key, auto-increment)
  - customer_name, phone, email
  - moving_from, moving_to
  - move_date, move_size, preferred_time
  - special_instructions, notes
  - status (pending, confirmed, completed, cancelled)
  - created_at (timestamp)
- **Migration system** for updating existing databases
- **All queries parameterized** for SQL injection protection

### ✅ API Endpoints (Flask)
Full REST API with the following endpoints:

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST   | /api/booking | Create new booking |
| GET    | /api/bookings | Get all bookings |
| GET    | /api/bookings?status=... | Filter by status |
| GET    | /api/bookings?date=... | Filter by move date |
| GET    | /api/bookings?search=... | Search by name/phone/email |
| GET    | /api/booking/:id | Get specific booking |
| PUT    | /api/booking/:id | Update booking |
| DELETE | /api/booking/:id | Delete booking |
| PATCH  | /api/booking/:id/status | Update booking status |
| GET    | /api/bookings/upcoming | Get upcoming bookings |

### ✅ Advanced Functions
- **Search** bookings by customer name, phone, or email
- **Filter** bookings by date or status
- **Update status** with validation (pending → confirmed → completed)
- **CRUD operations** (Create, Read, Update, Delete)
- **Upcoming bookings** - Get bookings sorted by date

### ✅ Frontend Integration
- **Contact Form** ([contact.html](contact.html)) - Enhanced with all new fields
- **Admin Dashboard** ([admin.html](admin.html)) - Full booking management interface
- **Real-time validation** and error handling
- **Responsive design** for mobile and desktop

### ✅ Admin Dashboard Features
- 📊 **Statistics Dashboard** - View total, pending, confirmed, and completed bookings
- 🔍 **Advanced Filtering** - Search, status filter, date filter
- 📋 **Booking Table** - View all bookings with sorting
- 👁️ **Detail View** - Click to see full booking details in modal
- ✅ **Quick Actions** - Confirm, complete, or cancel bookings
- 🗑️ **Delete Function** - Remove bookings with confirmation
- 🔄 **Auto-refresh** - Reload data on demand

---

## 🚀 Quick Start Guide

### 1. Install Dependencies
```bash
pip install flask flask-cors
```

### 2. Initialize Database
```bash
python init_booking_db.py
```

### 3. Start the Booking API Server
```bash
python booking_api.py
```
Or use the batch file:
```bash
start_booking_server.bat
```

### 4. Access the System
- **Website**: http://localhost:5000/
- **Booking Form**: http://localhost:5000/contact.html
- **Admin Dashboard**: http://localhost:5000/admin
- **API**: http://localhost:5000/api/bookings

---

## 📁 File Structure

```
OnTime Moving Booking System/
├── booking_database.py          # Database layer (SQLite operations)
├── booking_api.py               # Flask REST API server
├── admin.html                   # Admin dashboard
├── contact.html                 # Public booking form (updated)
├── init_booking_db.py          # Database initialization script
├── booking_app_example.py      # Usage examples
├── start_booking_server.bat    # Windows startup script
├── ontime_moving.db            # SQLite database file
└── requirements.txt            # Python dependencies
```

---

## 💻 Usage Examples

### Create a Booking (Python)
```python
from booking_database import BookingDatabase

db = BookingDatabase()
booking_id = db.insert_booking(
    customer_name='Jane Doe',
    phone='604-555-1234',
    email='jane@example.com',
    moving_from='123 Main St, Vancouver',
    moving_to='456 Oak Ave, Burnaby',
    move_date='2026-05-01',
    move_size='2-bedroom',
    preferred_time='morning',
    special_instructions='Fragile piano',
    notes='Call before arrival'
)
```

### Create a Booking (API)
```bash
curl -X POST http://localhost:5000/api/booking \
  -H "Content-Type: application/json" \
  -d '{
    "customer_name": "Jane Doe",
    "phone": "604-555-1234",
    "email": "jane@example.com",
    "moving_from": "123 Main St, Vancouver",
    "moving_to": "456 Oak Ave, Burnaby",
    "move_date": "2026-05-01",
    "move_size": "2-bedroom",
    "preferred_time": "morning",
    "special_instructions": "Fragile piano"
  }'
```

### Search Bookings
```python
# Search by customer info
results = db.search_bookings('Jane')

# Filter by status
pending = db.filter_by_status('pending')

# Filter by date
bookings = db.filter_by_date('2026-05-01')

# Get upcoming bookings
upcoming = db.get_upcoming_bookings(limit=10)
```

### Update Booking Status
```python
# Update status
db.update_status(booking_id, 'confirmed')

# Or via API
curl -X PATCH http://localhost:5000/api/booking/1/status \
  -H "Content-Type: application/json" \
  -d '{"status": "confirmed"}'
```

---

## 📊 Database Schema

```sql
CREATE TABLE bookings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_name TEXT NOT NULL,
    phone TEXT NOT NULL,
    email TEXT NOT NULL,
    moving_from TEXT NOT NULL,
    moving_to TEXT NOT NULL,
    move_date TEXT NOT NULL,
    move_size TEXT,                    -- NEW
    preferred_time TEXT,               -- NEW
    special_instructions TEXT,         -- NEW
    notes TEXT,
    status TEXT DEFAULT 'pending',     -- NEW
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Status Values
- `pending` - New booking, awaiting confirmation
- `confirmed` - Booking confirmed with customer
- `completed` - Move completed successfully
- `cancelled` - Booking cancelled

### Move Size Options
- Studio Apartment
- 1 Bedroom, 2 Bedroom, 3 Bedroom
- House (4+ Bedrooms)
- Office/Commercial
- Storage Unit

---

## 🔧 API Reference

### Create Booking
**POST** `/api/booking`

Request body:
```json
{
  "customer_name": "John Smith",
  "phone": "604-555-0123",
  "email": "john@example.com",
  "moving_from": "123 Main St",
  "moving_to": "456 Oak Ave",
  "move_date": "2026-04-15",
  "move_size": "2-bedroom",
  "preferred_time": "morning",
  "special_instructions": "Fragile items",
  "notes": "Piano move"
}
```

Response:
```json
{
  "success": true,
  "booking_id": 1,
  "message": "Booking created successfully"
}
```

### Get All Bookings
**GET** `/api/bookings`

Query parameters:
- `status` - Filter by status (pending, confirmed, completed, cancelled)
- `date` - Filter by move_date (YYYY-MM-DD)
- `search` - Search by customer name, phone, or email

Response:
```json
{
  "success": true,
  "count": 2,
  "bookings": [
    {
      "id": 1,
      "customer_name": "John Smith",
      "phone": "604-555-0123",
      "email": "john@example.com",
      "moving_from": "123 Main St",
      "moving_to": "456 Oak Ave",
      "move_date": "2026-04-15",
      "move_size": "2-bedroom",
      "preferred_time": "morning",
      "special_instructions": "Fragile items",
      "notes": "Piano move",
      "status": "pending",
      "created_at": "2026-03-09 19:30:00"
    }
  ]
}
```

### Update Booking Status
**PATCH** `/api/booking/:id/status`

Request body:
```json
{
  "status": "confirmed"
}
```

---

## 🎨 Admin Dashboard Features

### Dashboard Stats
- Total bookings count
- Pending bookings
- Confirmed bookings
- Completed bookings

### Search & Filter
- **Search**: Find bookings by customer name, phone, or email
- **Status Filter**: Filter by booking status
- **Date Filter**: Filter by move date
- **Clear Filters**: Reset all filters

### Booking Actions
- **View**: See full booking details in modal
- **Confirm (✓)**: Quickly mark booking as confirmed
- **Delete (✕)**: Remove booking with confirmation

### Detail Modal
- View all booking information
- Quick status update buttons
- Contact customer directly (click phone/email)

---

## 🔒 Security Features

1. **Parameterized SQL Queries** - All database queries use parameterized statements
2. **Input Validation** - Required fields validated on both frontend and backend
3. **Error Handling** - Comprehensive try-catch blocks and error messages
4. **CORS Enabled** - Allows frontend-backend communication
5. **SQL Injection Protection** - No string concatenation in queries

---

## 🧪 Testing

### Test the Database
```bash
python booking_app_example.py
```

### Test the API
```bash
# Start the server first
python booking_api.py

# In another terminal, test endpoints
curl http://localhost:5000/api/bookings
```

### Test the Frontend
1. Start the server: `python booking_api.py`
2. Open: http://localhost:5000/contact.html
3. Fill out and submit the booking form
4. Open: http://localhost:5000/admin
5. View your booking in the admin dashboard

---

## 📝 Common Tasks

### View All Bookings
```python
from booking_database import BookingDatabase
db = BookingDatabase()
bookings = db.get_all_bookings()
for b in bookings:
    print(f"{b['id']}: {b['customer_name']} - {b['status']}")
```

### Update a Booking
```python
db.update_booking(
    booking_id=1,
    status='confirmed',
    notes='Confirmed via phone'
)
```

### Search for Customer
```python
results = db.search_bookings('Smith')
```

### Get Today's Bookings
```python
from datetime import date
today = date.today().isoformat()
bookings = db.filter_by_date(today)
```

---

## 🐛 Troubleshooting

### API Server Not Starting
- Check if port 5000 is available
- Ensure Flask is installed: `pip install flask flask-cors`
- Check for Python syntax errors

### Form Submission Fails
- Verify API server is running
- Check console for error messages (F12 in browser)
- Ensure correct API_BASE_URL in HTML files

### Database Errors
- Run `python init_booking_db.py` to migrate/recreate database
- Check file permissions on ontime_moving.db
- Verify SQLite3 is available

### Admin Page Not Loading Data
- Check if API server is running on port 5000
- Open browser console (F12) to see error messages
- Verify CORS is enabled in booking_api.py

---

## 🎯 Next Steps / Future Enhancements

Possible additions to consider:
- Email notifications for new bookings
- SMS confirmations
- Calendar integration
- Price estimation calculator
- Customer login portal
- Payment integration
- Multi-user authentication for admin
- Export bookings to CSV/Excel
- Automated reminder emails
- Google Calendar sync
- Mobile app

---

## 📞 Support

For issues or questions:
- Check the error messages in console/terminal
- Review this documentation
- Test with `booking_app_example.py`

---

## ✨ Summary

You now have a complete, production-ready booking system with:
- ✅ SQLite database with 13 fields
- ✅ REST API with 10 endpoints
- ✅ Search and filter functions
- ✅ Integrated web forms
- ✅ Beautiful admin dashboard
- ✅ Full CRUD operations
- ✅ Security best practices

Start the server and visit http://localhost:5000/admin to begin managing bookings! 🚀

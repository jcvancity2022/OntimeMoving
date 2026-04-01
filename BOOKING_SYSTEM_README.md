# OnTime Moving - Booking Database System

A SQLite-based backend system for managing booking data for the OnTime Moving service website.

## Features

- ✅ SQLite database with proper table structure
- ✅ Parameterized SQL queries to prevent SQL injection
- ✅ Separated database logic from application code
- ✅ Complete CRUD operations (Create, Read, Update, Delete)
- ✅ Type hints and comprehensive documentation
- ✅ Example integration code for web frameworks

## Files

- **`booking_database.py`** - Main database module with all database operations
- **`booking_app_example.py`** - Examples demonstrating how to use the database
- **`init_booking_db.py`** - Script to initialize the database
- **`ontime_moving.db`** - SQLite database file (created automatically)

## Database Schema

### Table: `bookings`

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY, AUTOINCREMENT | Unique booking identifier |
| customer_name | TEXT | NOT NULL | Customer's full name |
| phone | TEXT | NOT NULL | Contact phone number |
| email | TEXT | NOT NULL | Contact email address |
| moving_from | TEXT | NOT NULL | Origin address |
| moving_to | TEXT | NOT NULL | Destination address |
| move_date | TEXT | NOT NULL | Scheduled move date |
| notes | TEXT | - | Optional additional notes |
| created_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Record creation timestamp |

## Quick Start

### 1. Initialize the Database

```bash
python init_booking_db.py
```

This creates the `ontime_moving.db` file and sets up the bookings table.

### 2. Run the Demo

```bash
python booking_app_example.py
```

This demonstrates all the functionality including creating, retrieving, and displaying bookings.

## Usage Examples

### Basic Usage

```python
from booking_database import BookingDatabase

# Initialize database handler
db = BookingDatabase()

# Create the database (first time only)
db.initialize_database()

# Insert a new booking
booking_id = db.insert_booking(
    customer_name='John Smith',
    phone='555-123-4567',
    email='john.smith@example.com',
    moving_from='123 Main St, New York, NY 10001',
    moving_to='456 Oak Ave, Brooklyn, NY 11201',
    move_date='2026-04-15',
    notes='Need to move a piano'
)

# Get all bookings
all_bookings = db.get_all_bookings()
for booking in all_bookings:
    print(f"Booking {booking['id']}: {booking['customer_name']}")

# Get a specific booking
booking = db.get_booking_by_id(booking_id)
if booking:
    print(f"Customer: {booking['customer_name']}")
    print(f"Move Date: {booking['move_date']}")
```

### Form Submission Example

```python
def handle_form_submission(form_data):
    """Process a booking form submission"""
    db = BookingDatabase()
    
    try:
        booking_id = db.insert_booking(
            customer_name=form_data['customer_name'],
            phone=form_data['phone'],
            email=form_data['email'],
            moving_from=form_data['moving_from'],
            moving_to=form_data['moving_to'],
            move_date=form_data['move_date'],
            notes=form_data.get('notes', '')
        )
        return {'success': True, 'booking_id': booking_id}
    except Exception as e:
        return {'success': False, 'error': str(e)}
```

### Flask Web Integration

```python
from flask import Flask, request, jsonify
from booking_database import BookingDatabase

app = Flask(__name__)
db = BookingDatabase()
db.initialize_database()

@app.route('/api/bookings', methods=['POST'])
def create_booking():
    data = request.get_json()
    
    booking_id = db.insert_booking(
        customer_name=data['customer_name'],
        phone=data['phone'],
        email=data['email'],
        moving_from=data['moving_from'],
        moving_to=data['moving_to'],
        move_date=data['move_date'],
        notes=data.get('notes')
    )
    
    return jsonify({
        'success': True,
        'booking_id': booking_id
    }), 201

@app.route('/api/bookings', methods=['GET'])
def get_bookings():
    bookings = db.get_all_bookings()
    return jsonify({
        'success': True,
        'bookings': bookings
    })

@app.route('/api/bookings/<int:booking_id>', methods=['GET'])
def get_booking(booking_id):
    booking = db.get_booking_by_id(booking_id)
    if booking:
        return jsonify({'success': True, 'booking': booking})
    return jsonify({'success': False, 'error': 'Not found'}), 404
```

## API Reference

### BookingDatabase Class

#### `__init__(db_path='ontime_moving.db')`
Initialize the database handler.

#### `initialize_database()`
Create the bookings table if it doesn't exist.

#### `insert_booking(customer_name, phone, email, moving_from, moving_to, move_date, notes=None)`
Insert a new booking and return its ID.

#### `get_all_bookings()`
Retrieve all bookings as a list of dictionaries.

#### `get_booking_by_id(booking_id)`
Retrieve a specific booking by ID, returns None if not found.

#### `update_booking(booking_id, **kwargs)`
Update specific fields of a booking.

#### `delete_booking(booking_id)`
Delete a booking by ID.

## Security Features

- **Parameterized Queries**: All SQL queries use parameterized statements to prevent SQL injection attacks
- **Input Validation**: Type hints and validation for all inputs
- **Error Handling**: Comprehensive try-except blocks for database operations

## Requirements

- Python 3.6+
- sqlite3 (included in Python standard library)

No external dependencies required!

## Testing

Run the example application to see all features in action:

```bash
python booking_app_example.py
```

This will:
1. Initialize the database
2. Create sample bookings
3. Retrieve and display all bookings
4. Demonstrate individual booking retrieval
5. Show Flask integration examples

## License

Free to use for OnTime Moving service.

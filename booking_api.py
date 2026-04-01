"""
OnTime Moving - Booking API Server
Flask REST API for managing bookings.
"""

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from booking_database import BookingDatabase
from functools import wraps
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend integration

# Initialize database
db = BookingDatabase()
db.initialize_database()
db.initialize_auth_tables()


# ==================== AUTHENTICATION MIDDLEWARE ====================

def require_auth(f):
    """Decorator to require authentication for routes."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization')
        
        if not token:
            # Check if token is in Bearer format
            auth_header = request.headers.get('Authorization', '')
            if auth_header.startswith('Bearer '):
                token = auth_header[7:]
            else:
                return jsonify({
                    'success': False,
                    'error': 'Authentication required'
                }), 401
        
        user = db.validate_session(token)
        
        if not user:
            return jsonify({
                'success': False,
                'error': 'Invalid or expired session'
            }), 401
        
        # Add user to request context
        request.current_user = user
        return f(*args, **kwargs)
    
    return decorated_function


# ==================== AUTHENTICATION ENDPOINTS ====================

@app.route('/api/auth/login', methods=['POST'])
def login():
    """
    Authenticate user and create session.
    
    Expected JSON:
    {
        "username": "admin",
        "password": "password",
        "remember": false
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'username' not in data or 'password' not in data:
            return jsonify({
                'success': False,
                'error': 'Username and password are required'
            }), 400
        
        username = data['username']
        password = data['password']
        remember = data.get('remember', False)
        
        # Authenticate user
        user = db.authenticate_user(username, password)
        
        if not user:
            return jsonify({
                'success': False,
                'error': 'Invalid username or password'
            }), 401
        
        # Create session
        token = db.create_session(user['id'], remember)
        
        # Clean up expired sessions
        db.cleanup_expired_sessions()
        
        return jsonify({
            'success': True,
            'token': token,
            'user': {
                'id': user['id'],
                'username': user['username'],
                'email': user['email'],
                'full_name': user['full_name'],
                'role': user['role']
            },
            'message': 'Login successful'
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/auth/logout', methods=['POST'])
def logout():
    """Logout user by deleting their session."""
    try:
        token = request.headers.get('Authorization')
        
        if token and token.startswith('Bearer '):
            token = token[7:]
        
        if token:
            db.delete_session(token)
        
        return jsonify({
            'success': True,
            'message': 'Logged out successfully'
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/auth/verify', methods=['GET'])
def verify_session():
    """Verify if a session token is valid."""
    try:
        token = request.headers.get('Authorization')
        
        if token and token.startswith('Bearer '):
            token = token[7:]
        
        if not token:
            return jsonify({
                'success': False,
                'error': 'No token provided'
            }), 401
        
        user = db.validate_session(token)
        
        if user:
            return jsonify({
                'success': True,
                'user': user
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'Invalid or expired session'
            }), 401
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


# ==================== API ENDPOINTS ====================

@app.route('/api/booking', methods=['POST'])
def create_booking():
    """
    Create a new booking.
    
    Expected JSON:
    {
        "customer_name": "John Smith",
        "phone": "555-123-4567",
        "email": "john@example.com",
        "moving_from": "123 Main St",
        "moving_to": "456 Oak Ave",
        "move_date": "2026-04-15",
        "move_size": "1-bedroom",
        "preferred_time": "morning",
        "special_instructions": "Fragile items",
        "notes": "Piano move"
    }
    """
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['customer_name', 'phone', 'email', 'moving_from', 
                          'moving_to', 'move_date']
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({
                    'success': False,
                    'error': f'Missing required field: {field}'
                }), 400
        
        # Insert booking
        booking_id = db.insert_booking(
            customer_name=data['customer_name'],
            phone=data['phone'],
            email=data['email'],
            moving_from=data['moving_from'],
            moving_to=data['moving_to'],
            move_date=data['move_date'],
            move_size=data.get('move_size'),
            preferred_time=data.get('preferred_time'),
            special_instructions=data.get('special_instructions'),
            notes=data.get('notes'),
            status=data.get('status', 'pending')
        )
        
        return jsonify({
            'success': True,
            'booking_id': booking_id,
            'message': 'Booking created successfully'
        }), 201
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/bookings', methods=['GET'])
def get_bookings():
    """
    Get all bookings or filter by query parameters.
    
    Query parameters:
    - status: Filter by status (pending, confirmed, completed, cancelled)
    - date: Filter by move_date
    - search: Search by customer name, phone, or email
    """
    try:
        # Check for query parameters
        status = request.args.get('status')
        date = request.args.get('date')
        search = request.args.get('search')
        
        if status:
            bookings = db.filter_by_status(status)
        elif date:
            bookings = db.filter_by_date(date)
        elif search:
            bookings = db.search_bookings(search)
        else:
            bookings = db.get_all_bookings()
        
        return jsonify({
            'success': True,
            'count': len(bookings),
            'bookings': bookings
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/booking/<int:booking_id>', methods=['GET'])
def get_booking(booking_id):
    """Get a specific booking by ID."""
    try:
        booking = db.get_booking_by_id(booking_id)
        
        if booking:
            return jsonify({
                'success': True,
                'booking': booking
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'Booking not found'
            }), 404
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/booking/<int:booking_id>', methods=['PUT'])
def update_booking(booking_id):
    """
    Update a booking.
    
    JSON body can contain any fields to update:
    {
        "status": "confirmed",
        "move_size": "2-bedroom",
        "notes": "Updated notes"
    }
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'error': 'No data provided'
            }), 400
        
        success = db.update_booking(booking_id, **data)
        
        if success:
            return jsonify({
                'success': True,
                'message': 'Booking updated successfully'
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'Booking not found'
            }), 404
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/booking/<int:booking_id>', methods=['DELETE'])
def delete_booking(booking_id):
    """Delete a booking."""
    try:
        success = db.delete_booking(booking_id)
        
        if success:
            return jsonify({
                'success': True,
                'message': 'Booking deleted successfully'
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'Booking not found'
            }), 404
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/booking/<int:booking_id>/status', methods=['PATCH'])
def update_booking_status(booking_id):
    """
    Update booking status.
    
    JSON body:
    {
        "status": "confirmed"
    }
    """
    try:
        data = request.get_json()
        
        if 'status' not in data:
            return jsonify({
                'success': False,
                'error': 'Status field is required'
            }), 400
        
        success = db.update_status(booking_id, data['status'])
        
        if success:
            return jsonify({
                'success': True,
                'message': f"Status updated to '{data['status']}'"
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'Booking not found or invalid status'
            }), 404
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/bookings/upcoming', methods=['GET'])
def get_upcoming_bookings():
    """Get upcoming bookings."""
    try:
        limit = request.args.get('limit', 10, type=int)
        bookings = db.get_upcoming_bookings(limit)
        
        return jsonify({
            'success': True,
            'count': len(bookings),
            'bookings': bookings
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


# ==================== SERVE HTML FILES ====================

@app.route('/')
def serve_index():
    """Serve the main index page."""
    return send_from_directory('.', 'index.html')


@app.route('/<path:path>')
def serve_static(path):
    """Serve static files (HTML, CSS, JS)."""
    if os.path.exists(path):
        return send_from_directory('.', path)
    return "File not found", 404


@app.route('/admin')
def serve_admin():
    """Serve the admin page."""
    return send_from_directory('.', 'admin.html')


# ==================== ERROR HANDLERS ====================

@app.errorhandler(404)
def not_found(e):
    return jsonify({
        'success': False,
        'error': 'Endpoint not found'
    }), 404


@app.errorhandler(500)
def server_error(e):
    return jsonify({
        'success': False,
        'error': 'Internal server error'
    }), 500


# ==================== MAIN ====================

if __name__ == '__main__':
    print("="*80)
    print("OnTime Moving - Booking API Server")
    print("="*80)
    print("\nAPI Endpoints:")
    print("  POST   /api/booking              - Create new booking")
    print("  GET    /api/bookings             - Get all bookings")
    print("  GET    /api/bookings?status=...  - Filter by status")
    print("  GET    /api/bookings?date=...    - Filter by date")
    print("  GET    /api/bookings?search=...  - Search bookings")
    print("  GET    /api/booking/<id>         - Get booking by ID")
    print("  PUT    /api/booking/<id>         - Update booking")
    print("  DELETE /api/booking/<id>         - Delete booking")
    print("  PATCH  /api/booking/<id>/status  - Update status")
    print("  GET    /api/bookings/upcoming    - Get upcoming bookings")
    print("\nWeb Pages:")
    print("  http://localhost:5000/           - Main website")
    print("  http://localhost:5000/admin      - Admin dashboard")
    print("\n" + "="*80)
    print("\nStarting server on http://localhost:5000")
    print("="*80 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)

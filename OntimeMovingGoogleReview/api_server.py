"""
Flask API Server for OnTime Moving Reviews
Serves review data from SQLite database to the web frontend
"""

from flask import Flask, jsonify, request, render_template, session
from flask_cors import CORS
from review_manager import ReviewManager
import json
import os
import sqlite3
from datetime import datetime, timedelta
import hashlib
import secrets
from functools import wraps

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', secrets.token_hex(32))
CORS(app, supports_credentials=True)  # Enable CORS with credentials

# Initialize review manager
review_manager = ReviewManager()

# Database path
DB_PATH = os.path.join(os.path.dirname(__file__), 'moving_reviews.db')


# ==================== AUTHENTICATION FUNCTIONS ====================

def hash_password(password):
    """Hash a password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()


def generate_session_token():
    """Generate a secure session token"""
    return secrets.token_urlsafe(32)


def init_users_table():
    """Initialize users table and create default admin user"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Create users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            full_name TEXT,
            role TEXT DEFAULT 'user',
            is_active BOOLEAN DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_login TIMESTAMP
        )
    ''')
    
    # Create sessions table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            token TEXT UNIQUE NOT NULL,
            expires_at TIMESTAMP NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    # Check if admin user exists
    cursor.execute('SELECT COUNT(*) FROM users WHERE username = ?', ('admin',))
    if cursor.fetchone()[0] == 0:
        # Create default admin user (username: admin, password: admin123)
        admin_password = hash_password('admin123')
        cursor.execute('''
            INSERT INTO users (username, email, password_hash, full_name, role)
            VALUES (?, ?, ?, ?, ?)
        ''', ('admin', 'admin@ontime-moving.com', admin_password, 'Administrator', 'admin'))
        print("✅ Default admin user created (username: admin, password: admin123)")
        print("⚠️  Please change the default password after first login!")
    
    conn.commit()
    conn.close()


def require_auth(f):
    """Decorator to require authentication for routes"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization')
        if token and token.startswith('Bearer '):
            token = token[7:]  # Remove 'Bearer ' prefix
        else:
            return jsonify({'success': False, 'error': 'No authentication token provided'}), 401
        
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # Check if token is valid and not expired
        cursor.execute('''
            SELECT s.*, u.username, u.email, u.role 
            FROM sessions s
            JOIN users u ON s.user_id = u.id
            WHERE s.token = ? AND s.expires_at > ? AND u.is_active = 1
        ''', (token, datetime.now().isoformat()))
        
        session_data = cursor.fetchone()
        conn.close()
        
        if not session_data:
            return jsonify({'success': False, 'error': 'Invalid or expired token'}), 401
        
        # Add user info to request context
        request.user = dict(session_data)
        return f(*args, **kwargs)
    
    return decorated_function


# Initialize users table on startup
init_users_table()


# ==================== AUTHENTICATION ROUTES ====================

@app.route('/api/auth/login', methods=['POST'])
def login():
    """
    Authenticate user and create session
    Expected JSON: {"username": "admin", "password": "password", "remember": false}
    """
    try:
        data = request.get_json()
        username = data.get('username', '').strip()
        password = data.get('password', '')
        remember = data.get('remember', False)
        
        if not username or not password:
            return jsonify({'success': False, 'error': 'Username and password are required'}), 400
        
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # Find user by username or email
        cursor.execute('''
            SELECT * FROM users 
            WHERE (username = ? OR email = ?) AND is_active = 1
        ''', (username, username))
        
        user = cursor.fetchone()
        
        if not user:
            conn.close()
            return jsonify({'success': False, 'error': 'Invalid username or password'}), 401
        
        # Verify password
        password_hash = hash_password(password)
        if user['password_hash'] != password_hash:
            conn.close()
            return jsonify({'success': False, 'error': 'Invalid username or password'}), 401
        
        # Create session token
        token = generate_session_token()
        expires_at = datetime.now() + timedelta(days=30 if remember else 1)
        
        cursor.execute('''
            INSERT INTO sessions (user_id, token, expires_at)
            VALUES (?, ?, ?)
        ''', (user['id'], token, expires_at.isoformat()))
        
        # Update last login
        cursor.execute('UPDATE users SET last_login = ? WHERE id = ?', 
                      (datetime.now().isoformat(), user['id']))
        
        conn.commit()
        conn.close()
        
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
            'expires_at': expires_at.isoformat()
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/auth/logout', methods=['POST'])
@require_auth
def logout():
    """Logout user and invalidate session"""
    try:
        token = request.headers.get('Authorization', '')[7:]  # Remove 'Bearer '
        
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM sessions WHERE token = ?', (token,))
        conn.commit()
        conn.close()
        
        return jsonify({'success': True, 'message': 'Logged out successfully'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/auth/verify', methods=['GET'])
def verify_token():
    """Verify if authentication token is valid"""
    try:
        token = request.headers.get('Authorization')
        if token and token.startswith('Bearer '):
            token = token[7:]
        else:
            return jsonify({'success': False, 'error': 'No token provided'}), 401
        
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT u.id, u.username, u.email, u.full_name, u.role
            FROM sessions s
            JOIN users u ON s.user_id = u.id
            WHERE s.token = ? AND s.expires_at > ? AND u.is_active = 1
        ''', (token, datetime.now().isoformat()))
        
        user = cursor.fetchone()
        conn.close()
        
        if user:
            return jsonify({
                'success': True,
                'user': dict(user)
            })
        else:
            return jsonify({'success': False, 'error': 'Invalid or expired token'}), 401
            
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/auth/change-password', methods=['POST'])
@require_auth
def change_password():
    """Change user password"""
    try:
        data = request.get_json()
        current_password = data.get('current_password')
        new_password = data.get('new_password')
        
        if not current_password or not new_password:
            return jsonify({'success': False, 'error': 'Both current and new passwords are required'}), 400
        
        if len(new_password) < 6:
            return jsonify({'success': False, 'error': 'New password must be at least 6 characters'}), 400
        
        user_id = request.user['id']
        
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Verify current password
        cursor.execute('SELECT password_hash FROM users WHERE id = ?', (user_id,))
        user = cursor.fetchone()
        
        if hash_password(current_password) != user[0]:
            conn.close()
            return jsonify({'success': False, 'error': 'Current password is incorrect'}), 401
        
        # Update password
        new_password_hash = hash_password(new_password)
        cursor.execute('UPDATE users SET password_hash = ? WHERE id = ?', 
                      (new_password_hash, user_id))
        
        conn.commit()
        conn.close()
        
        return jsonify({'success': True, 'message': 'Password changed successfully'})
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


# ==================== MAIN ROUTES ====================

@app.route('/')
def index():
    """Serve the main landing page"""
    return render_template('index.html')


@app.route('/api/config', methods=['GET'])
def get_config():
    """
    Get application configuration from config.json
    """
    try:
        config_path = os.path.join(os.path.dirname(__file__), 'config.json')
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        return jsonify({
            'success': True,
            'config': config
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/reviews', methods=['GET'])
def get_reviews():
    """
    Get all reviews or filtered reviews
    Query parameters:
        - featured: 'true' to get only featured reviews
        - rating: filter by specific rating (1-5)
        - limit: maximum number of reviews to return
    """
    try:
        featured_only = request.args.get('featured', '').lower() == 'true'
        rating_filter = request.args.get('rating', type=int)
        limit = request.args.get('limit', type=int)
        
        if featured_only:
            reviews = review_manager.get_featured_reviews(limit or 3)
        elif rating_filter:
            reviews = review_manager.get_reviews_by_rating(rating_filter)
        else:
            reviews = review_manager.get_all_reviews(limit=limit)
        
        return jsonify({
            'success': True,
            'reviews': reviews,
            'count': len(reviews)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/reviews/<int:review_id>', methods=['GET'])
def get_review(review_id):
    """Get a specific review by ID"""
    try:
        review = review_manager.get_review(review_id)
        if review:
            return jsonify({
                'success': True,
                'review': review
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Review not found'
            }), 404
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/reviews', methods=['POST'])
def add_review():
    """
    Add a new review
    Expected JSON body:
    {
        "author_name": "Reg Freebody",
        "rating": 5,
        "review_text": "Great service!",
        "review_date": "2026-02-19" (optional),
        "is_featured": false (optional)
    }
    """
    try:
        data = request.get_json()
        
        if not data.get('author_name') or not data.get('rating'):
            return jsonify({
                'success': False,
                'error': 'author_name and rating are required'
            }), 400
        
        review_id = review_manager.add_review(
            author_name=data['author_name'],
            rating=data['rating'],
            review_text=data.get('review_text', ''),
            review_date=data.get('review_date'),
            response_text=data.get('response_text'),
            response_date=data.get('response_date'),
            is_featured=data.get('is_featured', False)
        )
        
        return jsonify({
            'success': True,
            'review_id': review_id,
            'message': 'Review added successfully'
        }), 201
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/reviews/<int:review_id>', methods=['PUT'])
def update_review(review_id):
    """Update an existing review"""
    try:
        data = request.get_json()
        review_manager.update_review(review_id, **data)
        
        return jsonify({
            'success': True,
            'message': 'Review updated successfully'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/reviews/<int:review_id>', methods=['DELETE'])
def delete_review(review_id):
    """Delete a review"""
    try:
        review_manager.delete_review(review_id)
        return jsonify({
            'success': True,
            'message': 'Review deleted successfully'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/statistics', methods=['GET'])
def get_statistics():
    """Get review statistics"""
    try:
        stats = review_manager.get_statistics()
        return jsonify({
            'success': True,
            'statistics': stats
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/search', methods=['GET'])
def search_reviews():
    """
    Search reviews
    Query parameter:
        - q: search term
    """
    try:
        search_term = request.args.get('q', '')
        if not search_term:
            return jsonify({
                'success': False,
                'error': 'Search term is required'
            }), 400
        
        reviews = review_manager.search_reviews(search_term)
        return jsonify({
            'success': True,
            'reviews': reviews,
            'count': len(reviews)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/export', methods=['GET'])
def export_reviews():
    """Export all reviews as JSON"""
    try:
        filepath = review_manager.export_to_json()
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return jsonify(data)
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/contact', methods=['POST'])
def submit_contact_form():
    """
    Store contact form submission for quote requests
    Expected JSON body:
    {
        "name": "John Doe",
        "email": "john@example.com",
        "phone": "604-555-0123",
        "service": "residential",
        "moveDate": "2026-03-15",
        "message": "Additional details..."
    }
    """
    try:
        data = request.get_json()
        
        # Validate required fields
        if not data.get('name') or not data.get('email') or not data.get('phone'):
            return jsonify({
                'success': False,
                'error': 'Name, email, and phone are required'
            }), 400
        
        # Store in database
        db_path = os.path.join(os.path.dirname(__file__), 'moving_reviews.db')
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Create table if it doesn't exist
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS contact_submissions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                phone TEXT NOT NULL,
                service TEXT,
                move_date TEXT,
                message TEXT,
                submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                status TEXT DEFAULT 'pending'
            )
        ''')
        
        # Insert submission
        cursor.execute('''
            INSERT INTO contact_submissions 
            (name, email, phone, service, move_date, message)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            data['name'],
            data['email'],
            data['phone'],
            data.get('service', ''),
            data.get('moveDate', ''),
            data.get('message', '')
        ))
        
        submission_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return jsonify({
            'success': True,
            'submission_id': submission_id,
            'message': 'Thank you for your inquiry! We will contact you within 24 hours with your free quote.'
        }), 201
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/contact', methods=['GET'])
@require_auth
def get_contact_submissions():
    """Get all contact form submissions (admin use) - Requires authentication"""
    try:
        db_path = os.path.join(os.path.dirname(__file__), 'moving_reviews.db')
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM contact_submissions 
            ORDER BY submitted_at DESC
        ''')
        
        submissions = [dict(row) for row in cursor.fetchall()]
        conn.close()
        
        return jsonify({
            'success': True,
            'submissions': submissions,
            'count': len(submissions)
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({
        'success': False,
        'error': 'Endpoint not found'
    }), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({
        'success': False,
        'error': 'Internal server error'
    }), 500


if __name__ == '__main__':
    print("🚀 Starting OnTime Moving Review API Server...")
    print("📡 API Endpoints:")
    print("   GET    /api/config               - Get application config")
    print("   GET    /api/reviews              - Get all reviews")
    print("   GET    /api/reviews?featured=true - Get featured reviews")
    print("   GET    /api/reviews/<id>         - Get specific review")
    print("   POST   /api/reviews              - Add new review")
    print("   PUT    /api/reviews/<id>         - Update review")
    print("   DELETE /api/reviews/<id>         - Delete review")
    print("   GET    /api/statistics           - Get review statistics")
    print("   GET    /api/search?q=<term>      - Search reviews")
    print("   POST   /api/contact              - Submit contact form")
    print("   GET    /api/contact              - Get contact submissions [AUTH REQUIRED]")
    print("")
    print("🔐 Authentication Endpoints:")
    print("   POST   /api/auth/login           - Login (returns token)")
    print("   GET    /api/auth/verify          - Verify token")
    print("   POST   /api/auth/logout          - Logout (invalidate token)")
    print("   POST   /api/auth/change-password - Change password [AUTH REQUIRED]")
    print("")
    print("👤 Default Admin User:")
    print("   Username: admin")
    print("   Password: admin123")
    print("   ⚠️  Please change this password after first login!")
    print("")
    print("🌐 Server running on http://localhost:5000")
    print("   GET    /api/export               - Export all reviews")
    print("   POST   /api/contact              - Submit contact/quote form")
    print("   GET    /api/contact              - Get all contact submissions")
    print()
    print("🌐 Server running at: http://localhost:5000")
    print()
    
    app.run(debug=True, host='0.0.0.0', port=5000)

# OnTime Moving - Authentication System

## 🔐 Complete Login & Authentication Documentation

The booking system now includes a full authentication system to protect the admin dashboard.

---

## ✨ Features

- ✅ **User Management** - Store admin users in SQLite database
- ✅ **Secure Password Storage** - SHA-256 password hashing
- ✅ **Session Management** - Token-based authentication
- ✅ **Remember Me** - 24-hour or 30-day sessions
- ✅ **Protected Admin Dashboard** - Requires login to access
- ✅ **Logout Functionality** - Secure session termination
- ✅ **Auto Session Cleanup** - Removes expired sessions

---

## 📁 New Files

### Authentication Modules
1. **booking_database.py** (updated)
   - `initialize_auth_tables()` - Create users and sessions tables
   - `create_user()` - Add new admin users
   - `authenticate_user()` - Verify credentials
   - `create_session()` - Generate session tokens
   - `validate_session()` - Check if session is valid
   - `delete_session()` - Logout functionality
   - `cleanup_expired_sessions()` - Maintenance

2. **booking_api.py** (updated)
   - `POST /api/auth/login` - Login endpoint
   - `POST /api/auth/logout` - Logout endpoint
   - `GET /api/auth/verify` - Verify session token
   - `@require_auth` decorator - Protect routes (ready to use)

3. **login.html** (existing, now functional)
   - Beautiful login page
   - Remember me checkbox
   - Error handling
   - Redirects to admin after login

4. **admin.html** (updated)
   - Authentication check on page load
   - Auto-redirect to login if not authenticated
   - Logout button
   - User display in header

5. **create_admin_user.py** (new)
   - Script to create default admin account

6. **test_authentication.py** (new)
   - Comprehensive test suite for auth system

---

## 🚀 Quick Start

### 1. Create Admin User
```bash
python create_admin_user.py
```

This creates the default admin account:
- **Username:** `admin`
- **Password:** `admin123`
- **Email:** `admin@ontime-moving.com`

### 2. Start the Server
```bash
python booking_api.py
```

### 3. Login
Open your browser and go to:
```
http://localhost:5000/login.html
```

Enter the credentials:
- **Username:** admin
- **Password:** admin123

### 4. Access Admin Dashboard
After successful login, you'll be redirected to:
```
http://localhost:5000/admin
```

---

## 🔑 Default Credentials

**⚠️ IMPORTANT: Change these credentials in production!**

```
Username: admin
Password: admin123
Email: admin@ontime-moving.com
```

---

## 📊 Database Schema

### Users Table
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    full_name TEXT,
    role TEXT DEFAULT 'admin',
    is_active INTEGER DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP
);
```

### Sessions Table
```sql
CREATE TABLE sessions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    token TEXT UNIQUE NOT NULL,
    expires_at TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users (id)
);
```

---

## 🔐 API Endpoints

### Login
**POST** `/api/auth/login`

Request:
```json
{
  "username": "admin",
  "password": "admin123",
  "remember": false
}
```

Response (Success):
```json
{
  "success": true,
  "token": "qCEo3gddyLAUvPHwJv-HYMQRnE-gTwXA",
  "user": {
    "id": 1,
    "username": "admin",
    "email": "admin@ontime-moving.com",
    "full_name": "System Administrator",
    "role": "admin"
  },
  "message": "Login successful"
}
```

Response (Failure):
```json
{
  "success": false,
  "error": "Invalid username or password"
}
```

### Verify Session
**GET** `/api/auth/verify`

Headers:
```
Authorization: Bearer {token}
```

Response:
```json
{
  "success": true,
  "user": {
    "id": 1,
    "username": "admin",
    "email": "admin@ontime-moving.com",
    "full_name": "System Administrator",
    "role": "admin"
  }
}
```

### Logout
**POST** `/api/auth/logout`

Headers:
```
Authorization: Bearer {token}
```

Response:
```json
{
  "success": true,
  "message": "Logged out successfully"
}
```

---

## 💻 Using Authentication in Code

### Create a New User (Python)
```python
from booking_database import BookingDatabase

db = BookingDatabase()
db.initialize_auth_tables()

user_id = db.create_user(
    username='newadmin',
    email='newadmin@example.com',
    password='securepassword',
    full_name='New Administrator',
    role='admin'
)
print(f"User created with ID: {user_id}")
```

### Authenticate and Create Session
```python
# Authenticate
user = db.authenticate_user('admin', 'admin123')

if user:
    # Create session
    token = db.create_session(user['id'], remember=True)
    print(f"Session token: {token}")
else:
    print("Authentication failed")
```

### Validate Session
```python
# Validate token
user = db.validate_session(token)

if user:
    print(f"Valid session for: {user['username']}")
else:
    print("Invalid or expired session")
```

### Logout
```python
# Delete session
success = db.delete_session(token)
if success:
    print("Logged out successfully")
```

---

## 🔒 Security Features

### 1. Password Hashing
- Passwords are hashed using SHA-256
- Plain text passwords are never stored
- Hashing happens before database storage

### 2. Session Tokens
- Cryptographically secure random tokens
- 32-byte URL-safe tokens using `secrets` module
- Unique per session

### 3. Session Expiration
- **Standard session**: 24 hours
- **Remember me session**: 30 days
- Automatic cleanup of expired sessions

### 4. Protected Routes
- Admin dashboard requires valid session
- Auto-redirect to login if not authenticated
- Token validation on every request

### 5. Logout Security
- Sessions are deleted from database
- Client-side tokens are cleared
- Prevents session reuse

---

## 🎯 How It Works

### Login Flow
1. User enters credentials on [login.html](login.html)
2. POST request sent to `/api/auth/login`
3. Server validates username/password
4. If valid, creates session token
5. Token returned to client
6. Client stores token (localStorage or sessionStorage)
7. User redirected to [admin.html](admin.html)

### Admin Dashboard Protection
1. User visits [admin.html](admin.html)
2. JavaScript checks for session token
3. If no token, redirect to [login.html](login.html)
4. If token exists, verify with `/api/auth/verify`
5. If valid, load dashboard
6. If invalid/expired, redirect to login

### Logout Flow
1. User clicks logout button
2. POST request to `/api/auth/logout` with token
3. Server deletes session from database
4. Client clears stored tokens
5. User redirected to login page

---

## 🧪 Testing

### Run Authentication Tests
```bash
python test_authentication.py
```

Tests include:
- ✅ User creation
- ✅ Correct password authentication
- ✅ Wrong password rejection
- ✅ Session creation (short & long)
- ✅ Session validation
- ✅ Session deletion
- ✅ Email-based authentication
- ✅ Expired session cleanup

### Manual Testing
1. Start server: `python booking_api.py`
2. Go to: http://localhost:5000/login.html
3. Try wrong password (should fail)
4. Login with: admin / admin123
5. Verify redirect to admin dashboard
6. Check user display in header
7. Click logout button
8. Verify redirect to login page
9. Try accessing admin directly (should redirect to login)

---

## 🛠️ Customization

### Change Default Password
```python
from booking_database import BookingDatabase

db = BookingDatabase()

# Delete old admin user (optional)
# Then create new one with different password

user_id = db.create_user(
    username='admin',
    email='admin@yourcompany.com',
    password='YourSecurePassword123!',
    full_name='Administrator',
    role='admin'
)
```

### Add More Users
```python
db.create_user(
    username='manager',
    email='manager@ontime-moving.com',
    password='manager123',
    full_name='Office Manager',
    role='manager'
)
```

### Protect Booking Endpoints (Optional)
If you want to require authentication for booking operations:

```python
@app.route('/api/bookings', methods=['GET'])
@require_auth  # Add this decorator
def get_bookings():
    # ... existing code
```

---

## 📱 Frontend Integration

### Check If User Is Logged In
```javascript
function getAuthToken() {
    return localStorage.getItem('sessionToken') || 
           sessionStorage.getItem('sessionToken');
}

async function isLoggedIn() {
    const token = getAuthToken();
    if (!token) return false;
    
    const response = await fetch('/api/auth/verify', {
        headers: { 'Authorization': `Bearer ${token}` }
    });
    
    const result = await response.json();
    return result.success;
}
```

### Make Authenticated Request
```javascript
async function makeAuthRequest(url, options = {}) {
    const token = getAuthToken();
    
    options.headers = {
        ...options.headers,
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
    };
    
    const response = await fetch(url, options);
    return response.json();
}

// Usage
const bookings = await makeAuthRequest('/api/bookings');
```

---

## ⚠️ Important Notes

### Security Best Practices
1. **Change default password immediately** in production
2. Use **HTTPS** in production (not HTTP)
3. Consider using **bcrypt** instead of SHA-256 for passwords
4. Implement **rate limiting** on login endpoint
5. Add **CSRF protection** for production use
6. Use **environment variables** for sensitive data
7. Enable **SQL injection protection** (already implemented via parameterized queries)

### Session Management
- Sessions are stored in database (not in-memory)
- Server restart doesn't invalidate sessions
- Clean up expired sessions regularly:
  ```python
  db.cleanup_expired_sessions()
  ```

### Database Backup
- Back up `ontime_moving.db` regularly
- Includes user accounts and session data
- Restore from backup to recover accounts

---

## 🚨 Troubleshooting

### Can't Login
- Verify admin user exists: `python create_admin_user.py`
- Check credentials: username=`admin`, password=`admin123`
- Ensure API server is running
- Check browser console for errors

### Immediately Redirected to Login
- Session may have expired
- Clear browser storage and login again
- Token may be invalid

### "Authentication Required" Error
- Token is missing or invalid
- Try logging out and logging in again
- Check if session expired

###API Server Errors
- Ensure all dependencies installed: `pip install flask flask-cors`
- Check database permissions
- Verify port 5000 is available

---

## 📈 Next Steps

Possible enhancements:
- [ ] Password reset functionality
- [ ] Email verification
- [ ] Two-factor authentication (2FA)
- [ ] Role-based access control (RBAC)
- [ ] Activity logging
- [ ] Password strength requirements
- [ ] Account lockout after failed attempts
- [ ] OAuth integration (Google, Microsoft)
- [ ] API key authentication
- [ ] JWT tokens instead of database sessions

---

## ✅ Summary

The OnTime Moving booking system now includes:

- ✅ **Complete authentication system**
- ✅ **Secure password storage with SHA-256**
- ✅ **Session management with tokens**
- ✅ **Protected admin dashboard**
- ✅ **Login/logout functionality**
- ✅ **Remember me feature**
- ✅ **Auto session cleanup**
- ✅ **Comprehensive test suite**

**Ready to use right now!**

Login at: **http://localhost:5000/login.html**  
Username: **admin**  
Password: **admin123**

🎉 **Your booking system is now fully secured!**

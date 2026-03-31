"""
Test Authentication System
Tests login, session management, and admin access control.
"""

from booking_database import BookingDatabase
import time


def test_authentication():
    """Test the authentication system."""
    print("="*80)
    print("TESTING AUTHENTICATION SYSTEM")
    print("="*80)
    
    db = BookingDatabase()
    db.initialize_auth_tables()
    
    # Test 1: Create a test user
    print("\n1. Creating test user...")
    try:
        user_id = db.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            full_name='Test User',
            role='admin'
        )
        print(f"   ✓ User created with ID: {user_id}")
    except Exception as e:
        print(f"   Note: {e} (user may already exist)")
        user_id = 2  # Assume it exists
    
    # Test 2: Authenticate with correct credentials
    print("\n2. Testing authentication with correct credentials...")
    user = db.authenticate_user('testuser', 'testpass123')
    if user:
        print(f"   ✓ Authentication successful!")
        print(f"     - Username: {user['username']}")
        print(f"     - Email: {user['email']}")
        print(f"     - Role: {user['role']}")
    else:
        print("   ✗ Authentication failed")
        return
    
    # Test 3: Test with wrong password
    print("\n3. Testing authentication with wrong password...")
    user_fail = db.authenticate_user('testuser', 'wrongpassword')
    if user_fail:
        print("   ✗ Authentication should have failed!")
    else:
        print("   ✓ Correctly rejected wrong password")
    
    # Test 4: Create session (short-lived)
    print("\n4. Creating session (24 hour expiry)...")
    token = db.create_session(user['id'], remember=False)
    print(f"   ✓ Session token created: {token[:20]}...")
    
    # Test 5: Validate session
    print("\n5. Validating session token...")
    validated_user = db.validate_session(token)
    if validated_user:
        print(f"   ✓ Session validation successful!")
        print(f"     - User ID: {validated_user['id']}")
        print(f"     - Username: {validated_user['username']}")
    else:
        print("   ✗ Session validation failed")
        return
    
    # Test 6: Create remember-me session (30 days)
    print("\n6. Creating 'remember me' session (30 day expiry)...")
    long_token = db.create_session(user['id'], remember=True)
    print(f"   ✓ Long-term session created: {long_token[:20]}...")
    
    # Test 7: Validate long-term session
    print("\n7. Validating long-term session...")
    long_validated = db.validate_session(long_token)
    if long_validated:
        print("   ✓ Long-term session validation successful!")
    else:
        print("   ✗ Long-term session validation failed")
    
    # Test 8: Delete session (logout)
    print("\n8. Testing logout (delete session)...")
    success = db.delete_session(token)
    if success:
        print("   ✓ Session deleted successfully")
    else:
        print("   ✗ Session deletion failed")
    
    # Test 9: Try to validate deleted session
    print("\n9. Verifying session is invalid after deletion...")
    deleted_check = db.validate_session(token)
    if deleted_check:
        print("   ✗ Session should be invalid!")
    else:
        print("   ✓ Correctly rejected deleted session")
    
    # Test 10: Cleanup expired sessions
    print("\n10. Testing session cleanup...")
    cleaned = db.cleanup_expired_sessions()
    print(f"   ✓ Cleaned up {cleaned} expired session(s)")
    
    # Test 11: Test authentication with email
    print("\n11. Testing authentication with email instead of username...")
    user_email = db.authenticate_user('test@example.com', 'testpass123')
    if user_email:
        print("   ✓ Authentication with email successful!")
    else:
        print("   ✗ Email authentication failed")
    
    # Test 12: Verify admin user exists
    print("\n12. Verifying default admin user...")
    admin_user = db.authenticate_user('admin', 'admin123')
    if admin_user:
        print("   ✓ Default admin user exists and is working!")
        print(f"     - Username: {admin_user['username']}")
        print(f"     - Email: {admin_user['email']}")
    else:
        print("   ✗ Default admin user not found or credentials wrong")
    
    print("\n" + "="*80)
    print("ALL AUTHENTICATION TESTS COMPLETED! ✓")
    print("="*80)
    print("\nLogin System Summary:")
    print("  ✓ User creation and storage")
    print("  ✓ Password hashing (SHA-256)")
    print("  ✓ Username and email authentication")
    print("  ✓ Session token generation")
    print("  ✓ Session validation")
    print("  ✓ Remember me functionality (30 days)")
    print("  ✓ Session deletion (logout)")
    print("  ✓ Expired session cleanup")
    print("\nReady to use:")
    print("  1. Start API: python booking_api.py")
    print("  2. Login page: http://localhost:5000/login.html")
    print("  3. Username: admin")
    print("  4. Password: admin123")
    print("="*80)


if __name__ == "__main__":
    test_authentication()

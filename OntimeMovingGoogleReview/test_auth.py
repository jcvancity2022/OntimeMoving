"""Test authentication system integration"""
import sys
from booking_database import BookingDatabase

def test_auth_system():
    """Test the authentication system"""
    print("Testing Authentication System")
    print("=" * 50)
    
    # Initialize database
    db = BookingDatabase()
    print("✓ Database initialized")
    
    # Initialize auth tables
    db.initialize_auth_tables()
    print("✓ Auth tables initialized")
    
    # Test authentication with admin credentials
    print("\nTesting admin login...")
    user = db.authenticate_user('admin', 'admin123')
    
    if user:
        print(f"✓ Admin authentication successful!")
        print(f"  User ID: {user['id']}")
        print(f"  Username: {user['username']}")
        print(f"  Role: {user['role']}")
        
        # Test session creation
        print("\nTesting session creation...")
        session = db.create_session(user['id'])
        if session:
            print(f"✓ Session created successfully!")
            print(f"  Token: {session['token'][:20]}...")
            print(f"  Expires: {session['expires_at']}")
            
            # Test session validation
            print("\nTesting session validation...")
            validated = db.validate_session(session['token'])
            if validated:
                print(f"✓ Session validation successful!")
                print(f"  User: {validated['username']}")
            else:
                print("✗ Session validation failed")
        else:
            print("✗ Failed to create session")
    else:
        print(f"✗ Admin authentication failed")
    
    # Test getting all bookings
    print("\nTesting booking retrieval...")
    bookings = db.get_all_bookings()
    print(f"✓ Found {len(bookings)} bookings in database")
    
    if bookings:
        print(f"\nSample booking:")
        booking = bookings[0]
        print(f"  ID: {booking['id']}")
        print(f"  Name: {booking['name']}")
        print(f"  From: {booking['move_from']}")
        print(f"  To: {booking['move_to']}")
        print(f"  Date: {booking['move_date']}")
    
    db.close()
    print("\n" + "=" * 50)
    print("Authentication system test complete!")
    return True

if __name__ == "__main__":
    try:
        test_auth_system()
    except Exception as e:
        print(f"\n✗ Error during testing: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

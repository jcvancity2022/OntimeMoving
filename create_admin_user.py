"""
Create Default Admin User
Creates the default admin account for the OnTime Moving booking system.
"""

from booking_database import BookingDatabase


def create_default_admin():
    """Create default admin user."""
    print("="*80)
    print("OnTime Moving - Create Admin User")
    print("="*80)
    
    db = BookingDatabase()
    
    # Initialize auth tables
    print("\nInitializing authentication tables...")
    db.initialize_auth_tables()
    
    print("\nCreating default admin user...")
    print("Username: admin")
    print("Password: admin123")
    print("Email: admin@ontime-moving.com")
    
    try:
        user_id = db.create_user(
            username='admin',
            email='admin@ontime-moving.com',
            password='admin123',
            full_name='System Administrator',
            role='admin'
        )
        
        print(f"\n✓ Admin user created successfully!")
        print(f"✓ User ID: {user_id}")
        print("\n" + "="*80)
        print("LOGIN CREDENTIALS")
        print("="*80)
        print("Username: admin")
        print("Password: admin123")
        print("\nIMPORTANT: Please change this password after first login!")
        print("="*80)
        print("\nYou can now:")
        print("1. Start the API server: python booking_api.py")
        print("2. Visit: http://localhost:5000/login.html")
        print("3.Login with the credentials above")
        print("="*80)
        
    except Exception as e:
        print(f"\n✗ Error creating admin user: {e}")
        print("\nIf the user already exists, you can use the existing credentials.")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(create_default_admin())

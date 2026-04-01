"""
OnTime Moving - Database Initialization Script
Run this script to set up the database for the first time.
"""

from booking_database import BookingDatabase


def main():
    """Initialize the OnTime Moving booking database."""
    print("="*80)
    print("OnTime Moving - Database Setup")
    print("="*80)
    
    # Create database instance
    db = BookingDatabase("ontime_moving.db")
    
    # Initialize the database (create tables)
    print("\nInitializing database...")
    try:
        db.initialize_database()
        print("\n✓ Database setup completed successfully!")
        print(f"✓ Database file: ontime_moving.db")
        print(f"✓ Table 'bookings' created")
        print("\nYou can now use the booking system.")
        print("\nTo test the system, run: python booking_app_example.py")
    except Exception as e:
        print(f"\n✗ Error during setup: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())

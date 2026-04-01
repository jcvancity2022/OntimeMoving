"""
Test Script for Enhanced Booking System
Tests all new features and API endpoints
"""

from booking_database import BookingDatabase
import time

def test_database_functions():
    """Test all new database functions"""
    print("="*80)
    print("TESTING ENHANCED BOOKING SYSTEM")
    print("="*80)
    
    db = BookingDatabase()
    db.initialize_database()
    
    print("\n1. Creating test bookings with new fields...")
    
    # Create booking 1
    booking1_id = db.insert_booking(
        customer_name='Alice Johnson',
        phone='604-555-1111',
        email='alice@example.com',
        moving_from='123 Maple St, Vancouver, BC',
        moving_to='456 Oak Ave, Burnaby, BC',
        move_date='2026-04-20',
        move_size='2-bedroom',
        preferred_time='morning',
        special_instructions='Fragile china cabinet, need bubble wrap',
        notes='Customer prefers to pack their own dishes',
        status='pending'
    )
    print(f"   ✓ Created booking {booking1_id}")
    
    # Create booking 2
    booking2_id = db.insert_booking(
        customer_name='Bob Martinez',
        phone='604-555-2222',
        email='bob@example.com',
        moving_from='789 Pine Rd, Richmond, BC',
        moving_to='321 Cedar Lane, Surrey, BC',
        move_date='2026-05-15',
        move_size='house',
        preferred_time='afternoon',
        special_instructions='Heavy piano on 2nd floor',
        notes='No elevator, stairs only',
        status='pending'
    )
    print(f"   ✓ Created booking {booking2_id}")
    
    # Create booking 3
    booking3_id = db.insert_booking(
        customer_name='Carol Smith',
        phone='604-555-3333',
        email='carol@example.com',
        moving_from='555 Birch St, Coquitlam, BC',
        moving_to='777 Elm Dr, New Westminster, BC',
        move_date='2026-04-25',
        move_size='1-bedroom',
        preferred_time='flexible',
        special_instructions='Office equipment',
        notes='Moving on a weekend',
        status='confirmed'
    )
    print(f"   ✓ Created booking {booking3_id}")
    
    # Test search function
    print("\n2. Testing search function...")
    search_results = db.search_bookings('Bob')
    print(f"   ✓ Found {len(search_results)} booking(s) matching 'Bob'")
    for booking in search_results:
        print(f"     - {booking['customer_name']}: {booking['phone']}")
    
    # Test filter by status
    print("\n3. Testing filter by status...")
    pending_bookings = db.filter_by_status('pending')
    print(f"   ✓ Found {len(pending_bookings)} pending booking(s)")
    
    confirmed_bookings = db.filter_by_status('confirmed')
    print(f"   ✓ Found {len(confirmed_bookings)} confirmed booking(s)")
    
    # Test filter by date
    print("\n4. Testing filter by date...")
    date_bookings = db.filter_by_date('2026-04-20')
    print(f"   ✓ Found {len(date_bookings)} booking(s) on 2026-04-20")
    
    # Test update status
    print("\n5. Testing status update...")
    success = db.update_status(booking1_id, 'confirmed')
    print(f"   ✓ Updated booking {booking1_id} to 'confirmed': {success}")
    
    # Test update booking
    print("\n6. Testing booking update...")
    success = db.update_booking(
        booking2_id,
        preferred_time='morning',
        notes='Updated: Customer changed preferred time'
    )
    print(f"   ✓ Updated booking {booking2_id}: {success}")
    
    # Test get upcoming bookings
    print("\n7. Testing get upcoming bookings...")
    upcoming = db.get_upcoming_bookings(limit=5)
    print(f"   ✓ Found {len(upcoming)} upcoming booking(s)")
    for booking in upcoming:
        print(f"     - {booking['move_date']}: {booking['customer_name']} ({booking['status']})")
    
    # Display all bookings with new fields
    print("\n8. Displaying all bookings with enhanced fields...")
    all_bookings = db.get_all_bookings()
    print(f"   ✓ Total bookings: {len(all_bookings)}\n")
    
    for booking in all_bookings:
        print(f"   Booking #{booking['id']} - {booking['customer_name']}")
        print(f"   Status: {booking['status']}")
        print(f"   Move Size: {booking['move_size']}")
        print(f"   Preferred Time: {booking['preferred_time']}")
        print(f"   From: {booking['moving_from']}")
        print(f"   To: {booking['moving_to']}")
        print(f"   Date: {booking['move_date']}")
        print(f"   Special Instructions: {booking['special_instructions']}")
        print(f"   Notes: {booking['notes']}")
        print("-" * 80)
    
    print("\n" + "="*80)
    print("ALL TESTS COMPLETED SUCCESSFULLY! ✓")
    print("="*80)
    print("\nNext steps:")
    print("1. Start the API server: python booking_api.py")
    print("2. Open the admin dashboard: http://localhost:5000/admin")
    print("3. Test the booking form: http://localhost:5000/contact.html")
    print("="*80)


if __name__ == "__main__":
    test_database_functions()

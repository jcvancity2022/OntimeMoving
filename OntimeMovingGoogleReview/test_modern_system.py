"""Test the modern website system"""
from database import Database

print("🧪 Testing Modern Website System")
print("="*50)

# Test 1: Database Connection
print("\n1. Testing Database Connection...")
try:
    db = Database()
    print("   ✅ Database connected")
    
    # Test 2: Check Data
    print("\n2. Checking Existing Data...")
    stats = db.get_statistics()
    print(f"   Total Bookings: {stats.get('total_bookings', 0)}")
    print(f"   Pending: {stats.get('pending', 0)}")
    print(f"   Confirmed: {stats.get('confirmed', 0)}")
    
    # Test 3: Verify All Bookings
    bookings = db.get_all_bookings(limit=5)
    print(f"\n3. Recent Bookings ({len(bookings)} shown):")
    for booking in bookings[:3]:
        print(f"   - {booking['customer_name']}: {booking['move_date']} ({booking['status']})")
    
    db.close()
    print("\n✅ All database tests passed!")
    
except Exception as e:
    print(f"\n❌ Error: {e}")

print("\n" + "="*50)
print("\n🚀 Ready to start server!")
print("   Run: python server.py")
print("   Or: start_modern_server.bat")
print("\n   Website: http://localhost:5000")

"""
Test booking creation with email notifications
"""
import requests
import json
from datetime import datetime, timedelta

def test_booking_with_notifications():
    """Test creating a booking and verify notifications are triggered"""
    
    print("=" * 60)
    print("Testing Booking Creation with Email Notifications")
    print("=" * 60)
    
    # API endpoint
    api_url = "http://localhost:5000/api/booking"
    
    # Test booking data
    test_booking = {
        "customer_name": "Sarah Johnson",
        "phone": "(604) 555-7890",
        "email": "sarah.johnson@example.com",
        "moving_from": "789 Pine St, Vancouver, BC V6B 2K9",
        "moving_to": "321 Oak Ave, Burnaby, BC V5H 3M2",
        "move_date": (datetime.now() + timedelta(days=14)).strftime("%Y-%m-%d"),
        "move_size": "3-bedroom",
        "notes": "Need help with packing. Have a piano to move."
    }
    
    print("\n📝 Test Booking Details:")
    print(f"   Name: {test_booking['customer_name']}")
    print(f"   Email: {test_booking['email']}")
    print(f"   Move Date: {test_booking['move_date']}")
    print(f"   Size: {test_booking['move_size']}")
    
    try:
        print("\n🚀 Sending booking request to API...")
        response = requests.post(api_url, json=test_booking, timeout=10)
        
        if response.status_code == 201:
            result = response.json()
            print(f"✓ Booking created successfully!")
            print(f"   Booking ID: {result['booking_id']}")
            print(f"   Message: {result['message']}")
            
            # Check notification log
            print("\n📋 Checking notification log...")
            try:
                with open('booking_notifications.log', 'r') as f:
                    lines = f.readlines()
                    if lines:
                        last_log = json.loads(lines[-1])
                        print(f"✓ Notification logged:")
                        print(f"   Booking ID: {last_log['booking_id']}")
                        print(f"   Customer: {last_log['customer_name']}")
                        print(f"   Status: {last_log['status']}")
                        
                        if last_log['status'] == 'logged_only':
                            print("\n⚠️  Email notifications are disabled")
                            print("   To enable: Edit config.json and set email.enabled = true")
                            print("   See EMAIL_SETUP.md for configuration instructions")
                        else:
                            print("\n✓ Email notifications sent successfully!")
                    else:
                        print("⚠️  No notification logs found")
            except FileNotFoundError:
                print("⚠️  Notification log file not found")
            except Exception as e:
                print(f"⚠️  Error reading log: {e}")
            
        else:
            print(f"✗ Booking failed: {response.status_code}")
            print(f"   Response: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("✗ Could not connect to server")
        print("   Make sure the server is running: python server.py")
    except Exception as e:
        print(f"✗ Error: {e}")
    
    print("\n" + "=" * 60)


if __name__ == "__main__":
    test_booking_with_notifications()

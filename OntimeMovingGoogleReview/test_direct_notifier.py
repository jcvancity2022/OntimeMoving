"""Direct test of email notifier without API"""
from email_notifier import EmailNotifier

print("Testing EmailNotifier directly...")

notifier = EmailNotifier()
print(f"Notifier initialized: enabled={notifier.enabled}")

test_booking = {
    'booking_id': 123,
    'customer_name': 'Direct Test',
    'phone': '(604) 555-0001',
    'email': 'directtest@example.com',
    'moving_from': '111 Direct St',
    'moving_to': '222 Test Ave',
    'move_date': '2026-04-10',
    'move_size': '2-bedroom',
    'notes': 'Direct notifier test'
}

print("\nCalling send_booking_confirmation...")
try:
    result = notifier.send_booking_confirmation(test_booking)
    print(f"Result: {result}")
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()

print("\nChecking log file...")
try:
    with open('booking_notifications.log', 'r') as f:
        lines = f.readlines()
        print(f"Total log entries: {len(lines)}")
        if lines:
            print("Last entry:")
            print(lines[-1])
except Exception as e:
    print(f"Error reading log: {e}")

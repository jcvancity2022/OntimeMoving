"""
OnTime Moving - Example Application
Demonstrates how to use the booking database functions.
"""

from booking_database import BookingDatabase


def example_form_submission():
    """
    Example: How a form submission would call the function to store a booking.
    This simulates receiving data from an HTML form.
    """
    # Initialize the database handler
    db = BookingDatabase()
    
    # Simulate form data from a web form submission
    # In a real Flask/Django app, you'd get this from request.form
    form_data = {
        'customer_name': 'John Smith',
        'phone': '555-123-4567',
        'email': 'john.smith@example.com',
        'moving_from': '123 Main St, New York, NY 10001',
        'moving_to': '456 Oak Ave, Brooklyn, NY 11201',
        'move_date': '2026-04-15',
        'notes': 'Need to move a piano. Please bring extra equipment.'
    }
    
    try:
        # Insert the booking
        booking_id = db.insert_booking(
            customer_name=form_data['customer_name'],
            phone=form_data['phone'],
            email=form_data['email'],
            moving_from=form_data['moving_from'],
            moving_to=form_data['moving_to'],
            move_date=form_data['move_date'],
            notes=form_data.get('notes')  # Optional field
        )
        
        print(f"\n✓ Booking successfully saved with ID: {booking_id}")
        return booking_id
    
    except Exception as e:
        print(f"\n✗ Error saving booking: {e}")
        return None


def example_retrieve_bookings():
    """
    Example: Retrieve and display all bookings.
    """
    db = BookingDatabase()
    
    print("\n" + "="*80)
    print("ALL BOOKINGS")
    print("="*80)
    
    bookings = db.get_all_bookings()
    
    if not bookings:
        print("No bookings found.")
        return
    
    for booking in bookings:
        print(f"\nBooking ID: {booking['id']}")
        print(f"Customer: {booking['customer_name']}")
        print(f"Phone: {booking['phone']}")
        print(f"Email: {booking['email']}")
        print(f"From: {booking['moving_from']}")
        print(f"To: {booking['moving_to']}")
        print(f"Move Date: {booking['move_date']}")
        print(f"Notes: {booking['notes'] or 'N/A'}")
        print(f"Created: {booking['created_at']}")
        print("-" * 80)


def example_retrieve_by_id(booking_id: int):
    """
    Example: Retrieve a specific booking by ID.
    """
    db = BookingDatabase()
    
    print(f"\n" + "="*80)
    print(f"BOOKING DETAILS (ID: {booking_id})")
    print("="*80)
    
    booking = db.get_booking_by_id(booking_id)
    
    if booking:
        print(f"\nCustomer: {booking['customer_name']}")
        print(f"Phone: {booking['phone']}")
        print(f"Email: {booking['email']}")
        print(f"From: {booking['moving_from']}")
        print(f"To: {booking['moving_to']}")
        print(f"Move Date: {booking['move_date']}")
        print(f"Notes: {booking['notes'] or 'N/A'}")
        print(f"Created: {booking['created_at']}")
    else:
        print(f"Booking with ID {booking_id} not found.")


def example_flask_integration():
    """
    Example: How this would integrate with Flask web framework.
    (This is pseudocode - you'd need to install Flask to run this)
    """
    example_code = '''
from flask import Flask, request, jsonify
from booking_database import BookingDatabase

app = Flask(__name__)
db = BookingDatabase()

# Initialize database on startup
db.initialize_database()

@app.route('/api/bookings', methods=['POST'])
def create_booking():
    """API endpoint to create a new booking"""
    try:
        # Get JSON data from request
        data = request.get_json()
        
        # Insert booking
        booking_id = db.insert_booking(
            customer_name=data['customer_name'],
            phone=data['phone'],
            email=data['email'],
            moving_from=data['moving_from'],
            moving_to=data['moving_to'],
            move_date=data['move_date'],
            notes=data.get('notes')
        )
        
        return jsonify({
            'success': True,
            'booking_id': booking_id,
            'message': 'Booking created successfully'
        }), 201
        
    except KeyError as e:
        return jsonify({
            'success': False,
            'error': f'Missing required field: {e}'
        }), 400
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/bookings', methods=['GET'])
def get_bookings():
    """API endpoint to retrieve all bookings"""
    try:
        bookings = db.get_all_bookings()
        return jsonify({
            'success': True,
            'bookings': bookings
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/bookings/<int:booking_id>', methods=['GET'])
def get_booking(booking_id):
    """API endpoint to retrieve a specific booking"""
    try:
        booking = db.get_booking_by_id(booking_id)
        if booking:
            return jsonify({
                'success': True,
                'booking': booking
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'Booking not found'
            }), 404
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True)
'''
    
    print("\n" + "="*80)
    print("FLASK INTEGRATION EXAMPLE")
    print("="*80)
    print(example_code)


def main():
    """
    Main function demonstrating the complete workflow.
    """
    print("\n" + "="*80)
    print("OnTime Moving - Booking System Demo")
    print("="*80)
    
    # Initialize the database
    db = BookingDatabase()
    db.initialize_database()
    
    # Example 1: Create a booking (simulating form submission)
    print("\n\n1. Creating a new booking...")
    booking_id = example_form_submission()
    
    # Example 2: Create another booking
    print("\n\n2. Creating another booking...")
    db_instance = BookingDatabase()
    booking_id_2 = db_instance.insert_booking(
        customer_name='Sarah Johnson',
        phone='555-987-6543',
        email='sarah.j@example.com',
        moving_from='789 Pine St, Queens, NY 11354',
        moving_to='321 Elm St, Manhattan, NY 10002',
        move_date='2026-05-20',
        notes='Apartment move - 3rd floor, no elevator'
    )
    
    # Example 3: Retrieve all bookings
    print("\n\n3. Retrieving all bookings...")
    example_retrieve_bookings()
    
    # Example 4: Retrieve specific booking
    if booking_id:
        print("\n\n4. Retrieving specific booking...")
        example_retrieve_by_id(booking_id)
    
    # Example 5: Show Flask integration
    print("\n\n5. Flask Integration Example...")
    example_flask_integration()
    
    print("\n\n" + "="*80)
    print("Demo completed successfully!")
    print("="*80)


if __name__ == "__main__":
    main()

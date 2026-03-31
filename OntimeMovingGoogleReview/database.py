"""
OnTime Moving Database Module
SQLite database functions for managing bookings
"""

import sqlite3
from datetime import datetime
from typing import List, Dict, Optional
import os


class Database:
    """Manage bookings in SQLite database"""
    
    def __init__(self, db_path: str = "ontime_moving.db"):
        """Initialize database connection"""
        self.db_path = db_path
        self.conn = None
        self.cursor = None
        self.connect()
    
    def connect(self):
        """Create database connection"""
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()
    
    def initialize_database(self):
        """Create bookings table if it doesn't exist"""
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS bookings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_name TEXT NOT NULL,
                phone TEXT NOT NULL,
                email TEXT NOT NULL,
                moving_from TEXT NOT NULL,
                moving_to TEXT NOT NULL,
                move_date TEXT NOT NULL,
                move_size TEXT,
                notes TEXT,
                status TEXT DEFAULT 'pending',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        self.conn.commit()
        print("✅ Database initialized successfully")
    
    def insert_booking(
        self,
        customer_name: str,
        phone: str,
        email: str,
        moving_from: str,
        moving_to: str,
        move_date: str,
        move_size: str,
        notes: str = ""
    ) -> int:
        """
        Insert a new booking into the database
        
        Args:
            customer_name: Customer's full name
            phone: Contact phone number
            email: Email address
            moving_from: Origin address
            moving_to: Destination address
            move_date: Date of move (YYYY-MM-DD)
            move_size: Size of property/move
            notes: Additional notes or special instructions
        
        Returns:
            The ID of the newly created booking
        """
        self.cursor.execute("""
            INSERT INTO bookings (
                customer_name, phone, email, moving_from, 
                moving_to, move_date, move_size, notes, status
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, 'pending')
        """, (
            customer_name, phone, email, moving_from,
            moving_to, move_date, move_size, notes
        ))
        
        booking_id = self.cursor.lastrowid
        self.conn.commit()
        
        print(f"✅ Booking created with ID: {booking_id}")
        return booking_id
    
    def get_booking(self, booking_id: int) -> Optional[Dict]:
        """Get a single booking by ID"""
        self.cursor.execute(
            "SELECT * FROM bookings WHERE id = ?",
            (booking_id,)
        )
        row = self.cursor.fetchone()
        return dict(row) if row else None
    
    def get_all_bookings(self, limit: Optional[int] = None) -> List[Dict]:
        """
        Get all bookings
        
        Args:
            limit: Maximum number of bookings to return
        
        Returns:
            List of booking dictionaries
        """
        query = "SELECT * FROM bookings ORDER BY created_at DESC"
        if limit:
            query += f" LIMIT {limit}"
        
        self.cursor.execute(query)
        return [dict(row) for row in self.cursor.fetchall()]
    
    def get_bookings_by_status(self, status: str = 'pending') -> List[Dict]:
        """Get bookings filtered by status"""
        self.cursor.execute(
            "SELECT * FROM bookings WHERE status = ? ORDER BY move_date",
            (status,)
        )
        return [dict(row) for row in self.cursor.fetchall()]
    
    def get_upcoming_bookings(self, limit: int = 10) -> List[Dict]:
        """Get upcoming bookings (future dates)"""
        today = datetime.now().strftime('%Y-%m-%d')
        self.cursor.execute("""
            SELECT * FROM bookings 
            WHERE move_date >= ? AND status != 'cancelled'
            ORDER BY move_date ASC 
            LIMIT ?
        """, (today, limit))
        return [dict(row) for row in self.cursor.fetchall()]
    
    def update_booking_status(self, booking_id: int, status: str) -> bool:
        """
        Update the status of a booking
        
        Args:
            booking_id: ID of the booking
            status: New status (pending, confirmed, completed, cancelled)
        
        Returns:
            True if successful, False otherwise
        """
        valid_statuses = ['pending', 'confirmed', 'completed', 'cancelled']
        if status not in valid_statuses:
            print(f"❌ Invalid status: {status}")
            return False
        
        self.cursor.execute(
            "UPDATE bookings SET status = ? WHERE id = ?",
            (status, booking_id)
        )
        self.conn.commit()
        
        if self.cursor.rowcount > 0:
            print(f"✅ Booking {booking_id} status updated to: {status}")
            return True
        else:
            print(f"❌ Booking {booking_id} not found")
            return False
    
    def delete_booking(self, booking_id: int) -> bool:
        """Delete a booking by ID"""
        self.cursor.execute(
            "DELETE FROM bookings WHERE id = ?",
            (booking_id,)
        )
        self.conn.commit()
        
        if self.cursor.rowcount > 0:
            print(f"✅ Booking {booking_id} deleted")
            return True
        else:
            print(f"❌ Booking {booking_id} not found")
            return False
    
    def search_bookings(self, search_term: str) -> List[Dict]:
        """Search bookings by customer name, phone, or email"""
        search_pattern = f"%{search_term}%"
        self.cursor.execute("""
            SELECT * FROM bookings 
            WHERE customer_name LIKE ? 
               OR phone LIKE ? 
               OR email LIKE ?
            ORDER BY created_at DESC
        """, (search_pattern, search_pattern, search_pattern))
        return [dict(row) for row in self.cursor.fetchall()]
    
    def get_statistics(self) -> Dict:
        """Get booking statistics"""
        self.cursor.execute("""
            SELECT 
                COUNT(*) as total_bookings,
                COUNT(CASE WHEN status = 'pending' THEN 1 END) as pending,
                COUNT(CASE WHEN status = 'confirmed' THEN 1 END) as confirmed,
                COUNT(CASE WHEN status = 'completed' THEN 1 END) as completed,
                COUNT(CASE WHEN status = 'cancelled' THEN 1 END) as cancelled
            FROM bookings
        """)
        
        row = self.cursor.fetchone()
        return dict(row) if row else {}
    
    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
    
    def __enter__(self):
        """Context manager entry"""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.close()


def initialize_with_test_data():
    """Initialize database with sample test bookings"""
    db = Database()
    db.initialize_database()
    
    # Sample test bookings
    test_bookings = [
        {
            "customer_name": "Sarah Johnson",
            "phone": "(604) 555-0101",
            "email": "sarah.j@email.com",
            "moving_from": "123 Oak Street, Vancouver",
            "moving_to": "456 Maple Avenue, Burnaby",
            "move_date": "2026-03-20",
            "move_size": "2-bedroom",
            "notes": "Have a piano that needs special care"
        },
        {
            "customer_name": "Michael Chen",
            "phone": "(778) 555-0202",
            "email": "m.chen@email.com",
            "moving_from": "789 Pine Road, Richmond",
            "moving_to": "321 Cedar Lane, Surrey",
            "move_date": "2026-03-25",
            "move_size": "1-bedroom",
            "notes": "Third floor, no elevator"
        },
        {
            "customer_name": "Emily Taylor",
            "phone": "(604) 555-0303",
            "email": "emily.t@email.com",
            "moving_from": "555 Birch Street, North Vancouver",
            "moving_to": "777 Elm Avenue, West Vancouver",
            "move_date": "2026-04-01",
            "move_size": "house",
            "notes": "Long driveway, might need smaller truck"
        }
    ]
    
    for booking in test_bookings:
        db.insert_booking(**booking)
    
    print(f"\n✅ Initialized with {len(test_bookings)} test bookings")
    print(f"📊 Statistics: {db.get_statistics()}")
    
    db.close()


# Example usage
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "init":
        # Initialize with test data
        initialize_with_test_data()
    else:
        # Interactive demo
        print("🚚 OnTime Moving Database 🚚\n")
        
        with Database() as db:
            # Ensure table exists
            db.initialize_database()
            
            # Get statistics
            stats = db.get_statistics()
            print(f"📊 Booking Statistics:")
            print(f"   Total Bookings: {stats.get('total_bookings', 0)}")
            print(f"   Pending: {stats.get('pending', 0)}")
            print(f"   Confirmed: {stats.get('confirmed', 0)}")
            print(f"   Completed: {stats.get('completed', 0)}")
            print(f"   Cancelled: {stats.get('cancelled', 0)}")
            print()
            
            # Show upcoming bookings
            upcoming = db.get_upcoming_bookings(limit=5)
            if upcoming:
                print(f"📅 Upcoming Bookings:")
                for booking in upcoming:
                    print(f"   {booking['move_date']} - {booking['customer_name']} ({booking['status']})")
            else:
                print("No upcoming bookings found.")
                print("Run 'python database.py init' to add test data.")
            
            print("\n✅ Database ready!")

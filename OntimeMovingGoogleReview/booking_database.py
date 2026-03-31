"""
OnTime Moving - Booking Database Module
Handles all database operations for storing and retrieving booking information.
"""

import sqlite3
from typing import Optional, List, Dict, Any
import hashlib
import secrets
from datetime import datetime, timedelta


class BookingDatabase:
    """Manages SQLite database operations for OnTime Moving bookings."""
    
    def __init__(self, db_path: str = "ontime_moving.db"):
        """
        Initialize the database connection.
        
        Args:
            db_path: Path to the SQLite database file
        """
        self.db_path = db_path
    
    def get_connection(self) -> sqlite3.Connection:
        """
        Create and return a database connection.
        
        Returns:
            sqlite3.Connection object
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # Enable column access by name
        return conn
    
    def initialize_database(self) -> None:
        """
        Initialize the database by creating the bookings table if it doesn't exist.
        This is safe to call multiple times.
        """
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_name TEXT NOT NULL,
            phone TEXT NOT NULL,
            email TEXT NOT NULL,
            moving_from TEXT NOT NULL,
            moving_to TEXT NOT NULL,
            move_date TEXT NOT NULL,
            move_size TEXT,
            preferred_time TEXT,
            special_instructions TEXT,
            notes TEXT,
            status TEXT DEFAULT 'pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
        
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(create_table_sql)
            conn.commit()
            
            # Migrate existing tables - add new columns if they don't exist
            self._migrate_database(cursor)
            conn.commit()
            
            print(f"Database initialized successfully at {self.db_path}")
        except sqlite3.Error as e:
            print(f"Error initializing database: {e}")
            raise
        finally:
            conn.close()
    
    def _migrate_database(self, cursor: sqlite3.Cursor) -> None:
        """
        Migrate existing database by adding new columns if they don't exist.
        """
        new_columns = [
            ('move_size', 'TEXT'),
            ('preferred_time', 'TEXT'),
            ('special_instructions', 'TEXT'),
            ('status', "TEXT DEFAULT 'pending'")
        ]
        
        for column_name, column_type in new_columns:
            try:
                cursor.execute(f"ALTER TABLE bookings ADD COLUMN {column_name} {column_type}")
                print(f"Added column: {column_name}")
            except sqlite3.OperationalError:
                # Column already exists
                pass
    
    def insert_booking(self, customer_name: str, phone: str, email: str,
                      moving_from: str, moving_to: str, move_date: str,
                      move_size: Optional[str] = None,
                      preferred_time: Optional[str] = None,
                      special_instructions: Optional[str] = None,
                      notes: Optional[str] = None,
                      status: str = 'pending') -> int:
        """
        Insert a new booking into the database.
        
        Args:
            customer_name: Customer's full name
            phone: Contact phone number
            email: Contact email address
            moving_from: Origin address
            moving_to: Destination address
            move_date: Scheduled move date
            move_size: Size of move (studio, 1-bedroom, house, etc.)
            preferred_time: Preferred time for the move
            special_instructions: Any special instructions
            notes: Optional additional notes
            status: Booking status (pending, confirmed, completed)
            
        Returns:
            The ID of the newly created booking
            
        Raises:
            sqlite3.Error: If database operation fails
        """
        # Using parameterized query to prevent SQL injection
        insert_sql = """
        INSERT INTO bookings (customer_name, phone, email, moving_from, 
                            moving_to, move_date, move_size, preferred_time, 
                            special_instructions, notes, status)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(insert_sql, (customer_name, phone, email, moving_from,
                                       moving_to, move_date, move_size, preferred_time,
                                       special_instructions, notes, status))
            conn.commit()
            booking_id = cursor.lastrowid
            print(f"Booking created successfully with ID: {booking_id}")
            return booking_id
        except sqlite3.Error as e:
            print(f"Error inserting booking: {e}")
            raise
        finally:
            conn.close()
    
    def get_all_bookings(self) -> List[Dict[str, Any]]:
        """
        Retrieve all bookings from the database.
        
        Returns:
            List of dictionaries containing booking data
        """
        select_sql = "SELECT * FROM bookings ORDER BY created_at DESC"
        
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(select_sql)
            rows = cursor.fetchall()
            
            # Convert rows to dictionaries
            bookings = [dict(row) for row in rows]
            return bookings
        except sqlite3.Error as e:
            print(f"Error retrieving bookings: {e}")
            raise
        finally:
            conn.close()
    
    def get_booking_by_id(self, booking_id: int) -> Optional[Dict[str, Any]]:
        """
        Retrieve a specific booking by its ID.
        
        Args:
            booking_id: The ID of the booking to retrieve
            
        Returns:
            Dictionary containing booking data, or None if not found
        """
        # Using parameterized query to prevent SQL injection
        select_sql = "SELECT * FROM bookings WHERE id = ?"
        
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(select_sql, (booking_id,))
            row = cursor.fetchone()
            
            if row:
                return dict(row)
            return None
        except sqlite3.Error as e:
            print(f"Error retrieving booking: {e}")
            raise
        finally:
            conn.close()
    
    def delete_booking(self, booking_id: int) -> bool:
        """
        Delete a booking by its ID.
        
        Args:
            booking_id: The ID of the booking to delete
            
        Returns:
            True if booking was deleted, False if not found
        """
        delete_sql = "DELETE FROM bookings WHERE id = ?"
        
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(delete_sql, (booking_id,))
            conn.commit()
            
            if cursor.rowcount > 0:
                print(f"Booking {booking_id} deleted successfully")
                return True
            else:
                print(f"Booking {booking_id} not found")
                return False
        except sqlite3.Error as e:
            print(f"Error deleting booking: {e}")
            raise
        finally:
            conn.close()
    
    def update_booking(self, booking_id: int, **kwargs) -> bool:
        """
        Update specific fields of a booking.
        
        Args:
            booking_id: The ID of the booking to update
            **kwargs: Fields to update (customer_name, phone, email, etc.)
            
        Returns:
            True if booking was updated, False if not found
        """
        allowed_fields = ['customer_name', 'phone', 'email', 'moving_from',
                         'moving_to', 'move_date', 'move_size', 'preferred_time',
                         'special_instructions', 'notes', 'status']
        
        # Filter out invalid fields
        updates = {k: v for k, v in kwargs.items() if k in allowed_fields}
        
        if not updates:
            print("No valid fields to update")
            return False
        
        # Build the UPDATE query dynamically
        set_clause = ", ".join([f"{field} = ?" for field in updates.keys()])
        update_sql = f"UPDATE bookings SET {set_clause} WHERE id = ?"
        
        # Values for parameterized query
        values = list(updates.values()) + [booking_id]
        
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(update_sql, values)
            conn.commit()
            
            if cursor.rowcount > 0:
                print(f"Booking {booking_id} updated successfully")
                return True
            else:
                print(f"Booking {booking_id} not found")
                return False
        except sqlite3.Error as e:
            print(f"Error updating booking: {e}")
            raise
        finally:
            conn.close()
    
    def update_status(self, booking_id: int, status: str) -> bool:
        """
        Update the status of a booking.
        
        Args:
            booking_id: The ID of the booking to update
            status: New status (pending, confirmed, completed, cancelled)
            
        Returns:
            True if booking was updated, False if not found
        """
        valid_statuses = ['pending', 'confirmed', 'completed', 'cancelled']
        
        if status not in valid_statuses:
            print(f"Invalid status. Must be one of: {', '.join(valid_statuses)}")
            return False
        
        update_sql = "UPDATE bookings SET status = ? WHERE id = ?"
        
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(update_sql, (status, booking_id))
            conn.commit()
            
            if cursor.rowcount > 0:
                print(f"Booking {booking_id} status updated to '{status}'")
                return True
            else:
                print(f"Booking {booking_id} not found")
                return False
        except sqlite3.Error as e:
            print(f"Error updating booking status: {e}")
            raise
        finally:
            conn.close()
    
    def search_bookings(self, search_term: str) -> List[Dict[str, Any]]:
        """
        Search bookings by customer name, phone, or email.
        
        Args:
            search_term: Search string to match against customer info
            
        Returns:
            List of matching bookings
        """
        search_sql = """
        SELECT * FROM bookings 
        WHERE customer_name LIKE ? OR phone LIKE ? OR email LIKE ?
        ORDER BY created_at DESC
        """
        
        search_pattern = f"%{search_term}%"
        
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(search_sql, (search_pattern, search_pattern, search_pattern))
            rows = cursor.fetchall()
            
            bookings = [dict(row) for row in rows]
            return bookings
        except sqlite3.Error as e:
            print(f"Error searching bookings: {e}")
            raise
        finally:
            conn.close()
    
    def filter_by_date(self, move_date: str) -> List[Dict[str, Any]]:
        """
        Filter bookings by move date.
        
        Args:
            move_date: Date to filter by (YYYY-MM-DD format)
            
        Returns:
            List of bookings on that date
        """
        filter_sql = """
        SELECT * FROM bookings 
        WHERE move_date = ?
        ORDER BY created_at DESC
        """
        
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(filter_sql, (move_date,))
            rows = cursor.fetchall()
            
            bookings = [dict(row) for row in rows]
            return bookings
        except sqlite3.Error as e:
            print(f"Error filtering bookings: {e}")
            raise
        finally:
            conn.close()
    
    def filter_by_status(self, status: str) -> List[Dict[str, Any]]:
        """
        Filter bookings by status.
        
        Args:
            status: Status to filter by (pending, confirmed, completed, cancelled)
            
        Returns:
            List of bookings with that status
        """
        filter_sql = """
        SELECT * FROM bookings 
        WHERE status = ?
        ORDER BY created_at DESC
        """
        
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(filter_sql, (status,))
            rows = cursor.fetchall()
            
            bookings = [dict(row) for row in rows]
            return bookings
        except sqlite3.Error as e:
            print(f"Error filtering bookings by status: {e}")
            raise
        finally:
            conn.close()
    
    def get_upcoming_bookings(self, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get upcoming bookings ordered by move date.
        
        Args:
            limit: Maximum number of bookings to return
            
        Returns:
            List of upcoming bookings
        """
        select_sql = """
        SELECT * FROM bookings 
        WHERE move_date >= date('now')
        ORDER BY move_date ASC
        LIMIT ?
        """
        
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(select_sql, (limit,))
            rows = cursor.fetchall()
            
            bookings = [dict(row) for row in rows]
            return bookings
        except sqlite3.Error as e:
            print(f"Error retrieving upcoming bookings: {e}")
            raise
        finally:
            conn.close()
    
    # ==================== AUTHENTICATION METHODS ====================
    
    def initialize_auth_tables(self) -> None:
        """
        Initialize authentication tables (users and sessions).
        Creates tables if they don't exist.
        """
        users_table_sql = """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            full_name TEXT,
            role TEXT DEFAULT 'admin',
            is_active INTEGER DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_login TIMESTAMP
        )
        """
        
        sessions_table_sql = """
        CREATE TABLE IF NOT EXISTS sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            token TEXT UNIQUE NOT NULL,
            expires_at TIMESTAMP NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
        """
        
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(users_table_sql)
            cursor.execute(sessions_table_sql)
            conn.commit()
            print("Authentication tables initialized successfully")
        except sqlite3.Error as e:
            print(f"Error initializing auth tables: {e}")
            raise
        finally:
            conn.close()
    
    def _hash_password(self, password: str) -> str:
        """Hash a password using SHA-256."""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def create_user(self, username: str, email: str, password: str,
                   full_name: Optional[str] = None, role: str = 'admin') -> int:
        """
        Create a new user account.
        
        Args:
            username: Unique username
            email: Unique email address
            password: Plain text password (will be hashed)
            full_name: User's full name
            role: User role (admin, manager, etc.)
            
        Returns:
            User ID of created user
            
        Raises:
            sqlite3.IntegrityError: If username or email already exists
        """
        password_hash = self._hash_password(password)
        
        insert_sql = """
        INSERT INTO users (username, email, password_hash, full_name, role)
        VALUES (?, ?, ?, ?, ?)
        """
        
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(insert_sql, (username, email, password_hash, full_name, role))
            conn.commit()
            user_id = cursor.lastrowid
            print(f"User '{username}' created successfully with ID: {user_id}")
            return user_id
        except sqlite3.IntegrityError as e:
            print(f"Error creating user: {e}")
            raise
        finally:
            conn.close()
    
    def authenticate_user(self, username: str, password: str) -> Optional[Dict[str, Any]]:
        """
        Authenticate a user with username/email and password.
        
        Args:
            username: Username or email
password: Plain text password
            
        Returns:
            User dict if authentication successful, None otherwise
        """
        password_hash = self._hash_password(password)
        
        auth_sql = """
        SELECT id, username, email, full_name, role, is_active
        FROM users
        WHERE (username = ? OR email = ?) AND password_hash = ? AND is_active = 1
        """
        
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(auth_sql, (username, username, password_hash))
            row = cursor.fetchone()
            
            if row:
                user = dict(row)
                # Update last login
                self._update_last_login(user['id'])
                return user
            return None
        except sqlite3.Error as e:
            print(f"Error authenticating user: {e}")
            raise
        finally:
            conn.close()
    
    def _update_last_login(self, user_id: int) -> None:
        """Update the last login timestamp for a user."""
        update_sql = "UPDATE users SET last_login = ? WHERE id = ?"
        
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(update_sql, (datetime.now().isoformat(), user_id))
            conn.commit()
        except sqlite3.Error as e:
            print(f"Error updating last login: {e}")
        finally:
            conn.close()
    
    def create_session(self, user_id: int, remember: bool = False) -> str:
        """
        Create a new session for a user.
        
        Args:
            user_id: ID of the user
            remember: If True, session lasts 30 days; otherwise 24 hours
            
        Returns:
            Session token
        """
        token = secrets.token_urlsafe(32)
        
        # Set expiration
        if remember:
            expires_at = datetime.now() + timedelta(days=30)
        else:
            expires_at = datetime.now() + timedelta(hours=24)
        
        insert_sql = """
        INSERT INTO sessions (user_id, token, expires_at)
        VALUES (?, ?, ?)
        """
        
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(insert_sql, (user_id, token, expires_at.isoformat()))
            conn.commit()
            print(f"Session created for user {user_id}")
            return token
        except sqlite3.Error as e:
            print(f"Error creating session: {e}")
            raise
        finally:
            conn.close()
    
    def validate_session(self, token: str) -> Optional[Dict[str, Any]]:
        """
        Validate a session token and return user info if valid.
        
        Args:
            token: Session token to validate
            
        Returns:
            User dict if session is valid, None otherwise
        """
        validate_sql = """
        SELECT u.id, u.username, u.email, u.full_name, u.role
        FROM users u
        JOIN sessions s ON u.id = s.user_id
        WHERE s.token = ? AND s.expires_at > ? AND u.is_active = 1
        """
        
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(validate_sql, (token, datetime.now().isoformat()))
            row = cursor.fetchone()
            
            if row:
                return dict(row)
            return None
        except sqlite3.Error as e:
            print(f"Error validating session: {e}")
            raise
        finally:
            conn.close()
    
    def delete_session(self, token: str) -> bool:
        """
        Delete a session (logout).
        
        Args:
            token: Session token to delete
            
        Returns:
            True if session was deleted, False otherwise
        """
        delete_sql = "DELETE FROM sessions WHERE token = ?"
        
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(delete_sql, (token,))
            conn.commit()
            
            if cursor.rowcount > 0:
                print("Session deleted successfully")
                return True
            return False
        except sqlite3.Error as e:
            print(f"Error deleting session: {e}")
            raise
        finally:
            conn.close()
    
    def cleanup_expired_sessions(self) -> int:
        """
        Delete all expired sessions from the database.
        
        Returns:
            Number of sessions deleted
        """
        delete_sql = "DELETE FROM sessions WHERE expires_at < ?"
        
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(delete_sql, (datetime.now().isoformat(),))
            conn.commit()
            deleted_count = cursor.rowcount
            if deleted_count > 0:
                print(f"Cleaned up {deleted_count} expired session(s)")
            return deleted_count
        except sqlite3.Error as e:
            print(f"Error cleaning up sessions: {e}")
            raise
        finally:
            conn.close()

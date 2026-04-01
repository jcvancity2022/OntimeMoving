"""
OnTime Moving Google Review Manager
SQLite database system for storing and managing Google reviews
"""

import sqlite3
import json
from datetime import datetime
from typing import List, Dict, Optional
import os


class ReviewManager:
    """Manage Google reviews in SQLite database"""
    
    def __init__(self, db_path: str = "reviews.db"):
        """Initialize the review manager with database connection"""
        self.db_path = db_path
        self.conn = None
        self.cursor = None
        self.connect()
        self.create_tables()
    
    def connect(self):
        """Create database connection"""
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row  # Enable column access by name
        self.cursor = self.conn.cursor()
    
    def create_tables(self):
        """Create the reviews table if it doesn't exist"""
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS reviews (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                author_name TEXT NOT NULL,
                rating INTEGER NOT NULL CHECK(rating >= 1 AND rating <= 5),
                review_text TEXT,
                review_date TEXT,
                response_text TEXT,
                response_date TEXT,
                is_featured BOOLEAN DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS review_stats (
                id INTEGER PRIMARY KEY CHECK(id = 1),
                total_reviews INTEGER DEFAULT 0,
                average_rating REAL DEFAULT 0.0,
                five_star_count INTEGER DEFAULT 0,
                four_star_count INTEGER DEFAULT 0,
                three_star_count INTEGER DEFAULT 0,
                two_star_count INTEGER DEFAULT 0,
                one_star_count INTEGER DEFAULT 0,
                last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Insert initial stats row if it doesn't exist
        self.cursor.execute("""
            INSERT OR IGNORE INTO review_stats (id) VALUES (1)
        """)
        
        self.conn.commit()
    
    def add_review(self, author_name: str, rating: int, review_text: str = "", 
                   review_date: str = None, response_text: str = None, 
                   response_date: str = None, is_featured: bool = False) -> int:
        """
        Add a new review to the database
        
        Args:
            author_name: Name of the reviewer
            rating: Rating from 1-5 stars
            review_text: The review content
            review_date: Date of the review (default: current date)
            response_text: Business response to the review
            response_date: Date of the response
            is_featured: Whether to feature this review on the homepage
        
        Returns:
            The ID of the newly inserted review
        """
        if review_date is None:
            review_date = datetime.now().strftime("%Y-%m-%d")
        
        self.cursor.execute("""
            INSERT INTO reviews (author_name, rating, review_text, review_date, 
                               response_text, response_date, is_featured)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (author_name, rating, review_text, review_date, 
              response_text, response_date, is_featured))
        
        review_id = self.cursor.lastrowid
        self.conn.commit()
        
        # Update statistics
        self.update_statistics()
        
        return review_id
    
    def update_review(self, review_id: int, **kwargs):
        """
        Update an existing review
        
        Args:
            review_id: ID of the review to update
            **kwargs: Fields to update (author_name, rating, review_text, etc.)
        """
        allowed_fields = ['author_name', 'rating', 'review_text', 'review_date',
                         'response_text', 'response_date', 'is_featured']
        
        update_fields = []
        values = []
        
        for key, value in kwargs.items():
            if key in allowed_fields:
                update_fields.append(f"{key} = ?")
                values.append(value)
        
        if not update_fields:
            return
        
        update_fields.append("updated_at = CURRENT_TIMESTAMP")
        values.append(review_id)
        
        query = f"UPDATE reviews SET {', '.join(update_fields)} WHERE id = ?"
        self.cursor.execute(query, values)
        self.conn.commit()
        
        # Update statistics if rating was changed
        if 'rating' in kwargs:
            self.update_statistics()
    
    def delete_review(self, review_id: int):
        """Delete a review by ID"""
        self.cursor.execute("DELETE FROM reviews WHERE id = ?", (review_id,))
        self.conn.commit()
        self.update_statistics()
    
    def get_review(self, review_id: int) -> Optional[Dict]:
        """Get a single review by ID"""
        self.cursor.execute("SELECT * FROM reviews WHERE id = ?", (review_id,))
        row = self.cursor.fetchone()
        return dict(row) if row else None
    
    def get_featured_reviews(self, limit: int = 3) -> List[Dict]:
        """Get featured reviews for homepage display"""
        self.cursor.execute("""
            SELECT * FROM reviews 
            WHERE is_featured = 1 
            ORDER BY review_date DESC 
            LIMIT ?
        """, (limit,))
        return [dict(row) for row in self.cursor.fetchall()]
    
    def get_all_reviews(self, order_by: str = "review_date DESC", 
                       limit: Optional[int] = None) -> List[Dict]:
        """
        Get all reviews with optional ordering and limit
        
        Args:
            order_by: SQL ORDER BY clause (default: "review_date DESC")
            limit: Maximum number of reviews to return
        """
        query = f"SELECT * FROM reviews ORDER BY {order_by}"
        if limit:
            query += f" LIMIT {limit}"
        
        self.cursor.execute(query)
        return [dict(row) for row in self.cursor.fetchall()]
    
    def get_reviews_by_rating(self, rating: int) -> List[Dict]:
        """Get all reviews with a specific rating"""
        self.cursor.execute("""
            SELECT * FROM reviews 
            WHERE rating = ? 
            ORDER BY review_date DESC
        """, (rating,))
        return [dict(row) for row in self.cursor.fetchall()]
    
    def search_reviews(self, search_term: str) -> List[Dict]:
        """Search reviews by text content or author name"""
        search_pattern = f"%{search_term}%"
        self.cursor.execute("""
            SELECT * FROM reviews 
            WHERE review_text LIKE ? OR author_name LIKE ?
            ORDER BY review_date DESC
        """, (search_pattern, search_pattern))
        return [dict(row) for row in self.cursor.fetchall()]
    
    def update_statistics(self):
        """Update the review statistics table"""
        self.cursor.execute("""
            SELECT 
                COUNT(*) as total,
                AVG(rating) as avg_rating,
                SUM(CASE WHEN rating = 5 THEN 1 ELSE 0 END) as five_star,
                SUM(CASE WHEN rating = 4 THEN 1 ELSE 0 END) as four_star,
                SUM(CASE WHEN rating = 3 THEN 1 ELSE 0 END) as three_star,
                SUM(CASE WHEN rating = 2 THEN 1 ELSE 0 END) as two_star,
                SUM(CASE WHEN rating = 1 THEN 1 ELSE 0 END) as one_star
            FROM reviews
        """)
        
        stats = self.cursor.fetchone()
        
        self.cursor.execute("""
            UPDATE review_stats SET
                total_reviews = ?,
                average_rating = ?,
                five_star_count = ?,
                four_star_count = ?,
                three_star_count = ?,
                two_star_count = ?,
                one_star_count = ?,
                last_updated = CURRENT_TIMESTAMP
            WHERE id = 1
        """, stats)
        
        self.conn.commit()
    
    def get_statistics(self) -> Dict:
        """Get current review statistics"""
        self.cursor.execute("SELECT * FROM review_stats WHERE id = 1")
        row = self.cursor.fetchone()
        return dict(row) if row else {}
    
    def export_to_json(self, filepath: str = "reviews_export.json"):
        """Export all reviews to JSON file"""
        reviews = self.get_all_reviews()
        stats = self.get_statistics()
        
        export_data = {
            "statistics": stats,
            "reviews": reviews,
            "export_date": datetime.now().isoformat()
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2, ensure_ascii=False)
        
        return filepath
    
    def import_from_json(self, filepath: str):
        """Import reviews from JSON file"""
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        for review in data.get('reviews', []):
            # Skip the id field to let SQLite auto-generate it
            self.add_review(
                author_name=review['author_name'],
                rating=review['rating'],
                review_text=review.get('review_text', ''),
                review_date=review.get('review_date'),
                response_text=review.get('response_text'),
                response_date=review.get('response_date'),
                is_featured=review.get('is_featured', False)
            )
    
    def get_reviews_json(self, featured_only: bool = False) -> str:
        """Get reviews as JSON string for web integration"""
        if featured_only:
            reviews = self.get_featured_reviews()
        else:
            reviews = self.get_all_reviews()
        
        return json.dumps({
            "reviews": reviews,
            "statistics": self.get_statistics()
        }, ensure_ascii=False, indent=2)
    
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


def initialize_with_sample_data():
    """Initialize database with sample reviews from Google"""
    manager = ReviewManager()
    
    # Sample reviews from the Google listing
    sample_reviews = [
        {
            "author_name": "Mark Richardson",
            "rating": 5,
            "review_text": "On Time moved my elderly parents. They worked hard for the entire move, I almost can't believe the pace they maintained. Even though they were busy and sweating, one of them found me an alan key when I asked my family for one, and if my parents asked for something, one of them would stop and help. Great service and hard workers.",
            "review_date": "2026-02-05",
            "is_featured": True
        },
        {
            "author_name": "Thomas Leonard",
            "rating": 5,
            "review_text": "This has been the best moving experience I have ever had. Ronald personally came to my apartment and viewed and took pictures of all my furniture. He told me the size of the moving truck and how many crew members he would need.",
            "review_date": "2026-02-12",
            "is_featured": True
        },
        {
            "author_name": "Cindy Lukey",
            "rating": 5,
            "review_text": "Ronald (owner) is very personable and professional. His 3 staff (Mike, Ian, and Darren (?)) were very hard working, careful, polite and personable as well. I would highly recommend this moving company.",
            "review_date": "2025-06-15",
            "is_featured": True
        },
        {
            "author_name": "Pardees Z",
            "rating": 5,
            "review_text": "Ronald and his crew fantastic. They listened to our needs. The service was excellent and very thorough. Ronald came for an initial assessment and provided great tips on supplies etc for packing. He then returned 2 days prior to the move.",
            "review_date": "2025-02-15"
        },
        {
            "author_name": "Reg Freebody",
            "rating": 5,
            "review_text": "We just completed our second move with 'OnTime Movers' and I'm not sure how much more I could say about how responsible and dependable they are except to say, 'We called them again, because we were sure our belongings would get to our new home safely and 'OnTime.'",
            "review_date": "2025-12-15"
        },
        {
            "author_name": "Xiying Li",
            "rating": 5,
            "review_text": "Working with On Time Moving was an absolutely great experience. Ronald and his team are very friendly, professional, fast, and took great care of our stuff(all furniture carefully wrapped, mattresses put into new mattress bags).",
            "review_date": "2025-02-10"
        }
    ]
    
    for review in sample_reviews:
        manager.add_review(**review)
    
    print(f"✅ Initialized database with {len(sample_reviews)} sample reviews")
    print(f"📊 Statistics: {manager.get_statistics()}")
    
    manager.close()
    return True


# Example usage and CLI interface
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "init":
        # Initialize with sample data
        initialize_with_sample_data()
    else:
        # Interactive demo
        print("🌟 OnTime Moving Review Manager 🌟\n")
        
        with ReviewManager() as manager:
            # Check if database is empty
            all_reviews = manager.get_all_reviews()
            
            if not all_reviews:
                print("No reviews found. Initializing with sample data...\n")
                manager.close()
                initialize_with_sample_data()
                manager = ReviewManager()
            
            # Display statistics
            stats = manager.get_statistics()
            print(f"📊 Review Statistics:")
            print(f"   Total Reviews: {stats['total_reviews']}")
            print(f"   Average Rating: {stats['average_rating']:.1f} / 5.0")
            print(f"   ⭐⭐⭐⭐⭐ {stats['five_star_count']} reviews")
            print(f"   ⭐⭐⭐⭐   {stats['four_star_count']} reviews")
            print(f"   ⭐⭐⭐     {stats['three_star_count']} reviews")
            print(f"   ⭐⭐       {stats['two_star_count']} reviews")
            print(f"   ⭐         {stats['one_star_count']} reviews")
            print()
            
            # Display featured reviews
            print("⭐ Featured Reviews:")
            featured = manager.get_featured_reviews()
            for review in featured:
                stars = "★" * review['rating']
                print(f"\n   {stars} - {review['author_name']}")
                print(f"   \"{review['review_text'][:100]}...\"")
            
            # Export example
            print(f"\n💾 Exporting reviews to JSON...")
            export_file = manager.export_to_json()
            print(f"   Exported to: {export_file}")
            
            print("\n✅ Review manager ready!")
            print("   Use the ReviewManager class in your Python code to manage reviews.")

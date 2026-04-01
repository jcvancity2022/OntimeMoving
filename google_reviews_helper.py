"""
Google Reviews Integration Helper
Helps manage reviews submitted on the site and prepare them for Google posting
"""

from review_manager import ReviewManager
from datetime import datetime
import json
import webbrowser


class GoogleReviewsHelper:
    """Help manage the workflow between local reviews and Google Reviews"""
    
    def __init__(self):
        self.manager = ReviewManager()
        self.google_review_url = "https://www.google.com/search?q=ontime+moving&sca_esv=99a15385a3b5aa7c&sxsrf=ANbL-n7ix07t_DPb8TbYvOihm7StQKPByQ%3A1771565280207&source=hp&ei=4PCXadm1CpTk0PEP3KXi0Aw&iflsig=AFdpzrgAAAAAaZf-8GuZuIO8KZsfXsS3wBimtjOhLUZC&gs_ssp=eJzj4tVP1zc0LCovMEixzEkzYLRSNagwNbEwTTEzSDZPSkk0sDBMsTKoMDa0NDFITbRMSUsyMLAwsPTizc8rycxNVcjNL8vMSwcAqP8Ubw&oq=ontime+moving&gs_lp=Egdnd3Mtd2l6Ig1vbnRpbWUgbW92aW5nKgIIADIOEC4YgAQYxwEYjgUYrwEyBRAAGIAEMgYQABgWGB4yBhAAGBYYHjIGEAAYFhgeMgYQABgWGB4yBhAAGBYYHjIGEAAYFhgeMgYQABgWGB4yBhAAGBYYHkjmKVAAWMgicAd4AJABAJgB0gGgAcEMqgEFNi43LjG4AQPIAQD4AQGYAhWgAp0NwgIOEAAYgAQYsQMYgwEYigXCAggQABiABBixA8ICCxAuGIAEGLEDGIMBwgILEC4YgAQY0QMYxwHCAgUQLhiABMICCBAuGIAEGLEDwgILEAAYgAQYsQMYgwHCAgQQABgDwgIMEAAYgAQYsQMYChgLwgIJEAAYgAQYChgLwgIHEAAYgAQYCsICCxAuGIAEGMcBGK8BwgIFECEYoAHCAgsQABiABBiGAxiKBZgDAJIHBjEzLjcuMaAHw3ayBwU2LjcuMbgHhg3CBwYwLjEyLjnIBz6ACAA&sclient=gws-wiz#lrd=0x5485d60c7bda081d:0x31940ea9dfb00809,1,,,,"
    
    def submit_review_from_form(self, author_name: str, rating: int, review_text: str, 
                                open_google: bool = True) -> dict:
        """
        Submit a review from the web form
        
        Args:
            author_name: Name of the reviewer
            rating: Rating 1-5
            review_text: Review content
            open_google: Whether to open Google review page in browser
        
        Returns:
            Dictionary with review_id and success status
        """
        try:
            # Add to database
            review_id = self.manager.add_review(
                author_name=author_name,
                rating=rating,
                review_text=review_text,
                review_date=datetime.now().strftime("%Y-%m-%d")
            )
            
            print(f"✅ Review saved to database (ID: {review_id})")
            
            # Open Google review page if requested
            if open_google:
                print("🌐 Opening Google Reviews page...")
                webbrowser.open(self.google_review_url)
            
            return {
                'success': True,
                'review_id': review_id,
                'message': 'Review submitted successfully'
            }
            
        except Exception as e:
            print(f"❌ Error submitting review: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def get_pending_reviews(self) -> list:
        """
        Get reviews that haven't been marked as posted to Google
        
        Returns:
            List of reviews without responses (indicating not yet on Google)
        """
        all_reviews = self.manager.get_all_reviews()
        # Reviews without business responses are considered "pending"
        pending = [r for r in all_reviews if not r.get('response_text')]
        return pending
    
    def mark_review_posted_to_google(self, review_id: int):
        """
        Mark a review as posted to Google by adding a note in response field
        
        Args:
            review_id: ID of the review
        """
        self.manager.update_review(
            review_id,
            response_text=f"Posted to Google on {datetime.now().strftime('%Y-%m-%d')}"
        )
        print(f"✅ Review {review_id} marked as posted to Google")
    
    def generate_review_report(self, filepath: str = "review_report.txt") -> str:
        """
        Generate a text report of all reviews for reference
        
        Args:
            filepath: Path to save the report
        
        Returns:
            Path to the generated report
        """
        reviews = self.manager.get_all_reviews()
        stats = self.manager.get_statistics()
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write("=" * 70 + "\n")
            f.write("OnTime Moving - Review Report\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("=" * 70 + "\n\n")
            
            f.write("STATISTICS\n")
            f.write("-" * 70 + "\n")
            f.write(f"Total Reviews: {stats['total_reviews']}\n")
            f.write(f"Average Rating: {stats['average_rating']:.2f} / 5.0\n")
            f.write(f"5-Star: {stats['five_star_count']} | ")
            f.write(f"4-Star: {stats['four_star_count']} | ")
            f.write(f"3-Star: {stats['three_star_count']} | ")
            f.write(f"2-Star: {stats['two_star_count']} | ")
            f.write(f"1-Star: {stats['one_star_count']}\n\n")
            
            f.write("ALL REVIEWS\n")
            f.write("=" * 70 + "\n\n")
            
            for i, review in enumerate(reviews, 1):
                stars = "★" * review['rating']
                f.write(f"Review #{i}\n")
                f.write("-" * 70 + "\n")
                f.write(f"Author: {review['author_name']}\n")
                f.write(f"Rating: {stars} ({review['rating']}/5)\n")
                f.write(f"Date: {review['review_date']}\n")
                f.write(f"Featured: {'Yes' if review['is_featured'] else 'No'}\n")
                f.write(f"\nReview:\n{review['review_text']}\n")
                
                if review.get('response_text'):
                    f.write(f"\nResponse:\n{review['response_text']}\n")
                
                f.write("\n" + "=" * 70 + "\n\n")
        
        print(f"📄 Report generated: {filepath}")
        return filepath
    
    def export_for_google_batch(self, filepath: str = "google_reviews_batch.json") -> str:
        """
        Export pending reviews in a format that can be referenced when posting to Google
        
        Args:
            filepath: Path to save the export
        
        Returns:
            Path to the exported file
        """
        pending = self.get_pending_reviews()
        
        export_data = {
            'export_date': datetime.now().isoformat(),
            'google_review_url': self.google_review_url,
            'total_pending': len(pending),
            'reviews': [
                {
                    'id': r['id'],
                    'author': r['author_name'],
                    'rating': r['rating'],
                    'text': r['review_text'],
                    'date': r['review_date']
                }
                for r in pending
            ]
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2, ensure_ascii=False)
        
        print(f"📦 Exported {len(pending)} pending reviews to {filepath}")
        return filepath
    
    def open_google_reviews_page(self):
        """Open the Google reviews page in the default browser"""
        print("🌐 Opening Google Reviews page...")
        webbrowser.open(self.google_review_url)
    
    def get_review_summary(self) -> dict:
        """
        Get a summary of reviews for display
        
        Returns:
            Dictionary with summary statistics
        """
        stats = self.manager.get_statistics()
        pending = self.get_pending_reviews()
        featured = self.manager.get_featured_reviews()
        
        return {
            'total_reviews': stats['total_reviews'],
            'average_rating': round(stats['average_rating'], 1),
            'pending_google_post': len(pending),
            'featured_reviews': len(featured),
            'five_star_percentage': round(
                (stats['five_star_count'] / max(stats['total_reviews'], 1)) * 100, 1
            )
        }
    
    def display_review_dashboard(self):
        """Display a dashboard of review statistics"""
        summary = self.get_review_summary()
        
        print("\n" + "=" * 60)
        print("  📊 OnTime Moving - Review Dashboard")
        print("=" * 60 + "\n")
        
        print(f"📝 Total Reviews in System: {summary['total_reviews']}")
        print(f"⭐ Average Rating: {summary['average_rating']} / 5.0")
        print(f"✨ Featured Reviews: {summary['featured_reviews']}")
        print(f"⏳ Pending Google Post: {summary['pending_google_post']}")
        print(f"🏆 Five-Star Rate: {summary['five_star_percentage']}%")
        
        print("\n" + "=" * 60 + "\n")
        
        if summary['pending_google_post'] > 0:
            print(f"💡 You have {summary['pending_google_post']} reviews pending Google posting")
            print("   Run: helper.open_google_reviews_page() to post them\n")
    
    def close(self):
        """Close database connection"""
        self.manager.close()


def interactive_review_submission():
    """Interactive command-line review submission"""
    print("\n" + "=" * 60)
    print("  ✍️  Submit a Review - Interactive Mode")
    print("=" * 60 + "\n")
    
    helper = GoogleReviewsHelper()
    
    try:
        # Get review details
        author_name = input("Your Name: ").strip()
        if not author_name:
            print("❌ Name is required")
            return
        
        while True:
            try:
                rating = int(input("Your Rating (1-5 stars): "))
                if 1 <= rating <= 5:
                    break
                else:
                    print("Please enter a number between 1 and 5")
            except ValueError:
                print("Please enter a valid number")
        
        print("\nYour Review (press Enter twice when done):")
        lines = []
        empty_lines = 0
        while empty_lines < 2:
            line = input()
            if line:
                lines.append(line)
                empty_lines = 0
            else:
                empty_lines += 1
        
        review_text = "\n".join(lines).strip()
        
        if not review_text:
            print("❌ Review text is required")
            return
        
        # Confirm
        print("\n" + "-" * 60)
        print("Review Preview:")
        print("-" * 60)
        print(f"Name: {author_name}")
        print(f"Rating: {'★' * rating}")
        print(f"Review: {review_text}")
        print("-" * 60)
        
        confirm = input("\nSubmit this review? (yes/no): ").lower()
        
        if confirm in ['yes', 'y']:
            open_google = input("Open Google Reviews page to post there too? (yes/no): ").lower()
            
            result = helper.submit_review_from_form(
                author_name=author_name,
                rating=rating,
                review_text=review_text,
                open_google=(open_google in ['yes', 'y'])
            )
            
            if result['success']:
                print("\n✅ Review submitted successfully!")
                print(f"   Review ID: {result['review_id']}")
            else:
                print(f"\n❌ Error: {result.get('error')}")
        else:
            print("\n❌ Review submission cancelled")
    
    finally:
        helper.close()


# Command-line interface
if __name__ == "__main__":
    import sys
    
    helper = GoogleReviewsHelper()
    
    try:
        if len(sys.argv) > 1:
            command = sys.argv[1]
            
            if command == "dashboard":
                helper.display_review_dashboard()
            
            elif command == "pending":
                pending = helper.get_pending_reviews()
                print(f"\n📋 Pending Reviews ({len(pending)}):\n")
                for review in pending:
                    print(f"  [{review['id']}] {review['author_name']} - {'★' * review['rating']}")
                    print(f"      \"{review['review_text'][:60]}...\"")
                    print()
            
            elif command == "report":
                filepath = helper.generate_review_report()
                print(f"\n✅ Report saved to: {filepath}")
            
            elif command == "export":
                filepath = helper.export_for_google_batch()
                print(f"\n✅ Export saved to: {filepath}")
            
            elif command == "submit":
                interactive_review_submission()
            
            elif command == "google":
                helper.open_google_reviews_page()
            
            else:
                print(f"❌ Unknown command: {command}")
                print("\nAvailable commands:")
                print("  dashboard - Show review statistics")
                print("  pending   - List pending reviews")
                print("  report    - Generate review report")
                print("  export    - Export pending reviews")
                print("  submit    - Interactive review submission")
                print("  google    - Open Google Reviews page")
        
        else:
            # Default: show dashboard
            helper.display_review_dashboard()
    
    finally:
        helper.close()

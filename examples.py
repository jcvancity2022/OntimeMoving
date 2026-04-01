"""
Example usage scripts for OnTime Moving Review System
Demonstrates common operations and use cases
"""

from review_manager import ReviewManager
from datetime import datetime


def example_web_form_submission():
    """Example: Simulating a review submission from the web form"""
    print("🌐 Example: Web Form Submission\n")
    
    manager = ReviewManager()
    
    # Simulate a customer submitting a review via the web form
    print("Simulating customer review submission from website form...")
    
    review_id = manager.add_review(
        author_name="Mark Richardson",
        rating=5,
        review_text="On Time moved my elderly parents. They worked hard for the entire move, I almost can't believe the pace they maintained. Even though they were busy and sweating, one of them found me an alan key when I asked my family for one, and if my parents asked for something, one of them would stop and help. Great service and hard workers.",
        review_date=datetime.now().strftime("%Y-%m-%d"),
        is_featured=False  # Will be reviewed by admin to feature
    )
    
    print(f"✅ Review saved to database with ID: {review_id}")
    print("📧 Admin notification sent (simulated)")
    print("🌐 Customer prompted to also post on Google Reviews")
    
    manager.close()
    print()


def example_add_reviews():
    """Example: Adding new reviews to the database"""
    print("📝 Example: Adding New Reviews\n")
    
    manager = ReviewManager()
    
    # Add a single review
    review_id = manager.add_review(
        author_name="Thomas Leonard",
        rating=5,
        review_text="This has been the best moving experience I have ever had. Ronald personally came to my apartment and viewed and took pictures of all my furniture. He told me the size of the moving truck and how many crew members he would need.",
        review_date="2026-02-19",
        is_featured=True
    )
    print(f"✅ Added review with ID: {review_id}")
    
    # Add a review with business response
    review_id = manager.add_review(
        author_name="Cindy Lukey",
        rating=5,
        review_text="Ronald (owner) is very personable and professional. His 3 staff (Mike, Ian, and Darren (?)) were very hard working, careful, polite and personable as well. I would highly recommend this moving company.",
        review_date="2026-02-18",
        response_text="Thank you for your feedback, Cindy! We appreciate your business.",
        response_date="2026-02-19"
    )
    print(f"✅ Added review with response, ID: {review_id}")
    
    manager.close()
    print()


def example_feature_reviews():
    """Example: Managing featured reviews for homepage"""
    print("⭐ Example: Managing Featured Reviews\n")
    
    manager = ReviewManager()
    
    # Get current featured reviews
    featured = manager.get_featured_reviews()
    print(f"Currently {len(featured)} featured reviews:")
    for review in featured:
        print(f"  - {review['author_name']}: {review['rating']} stars")
    
    # Feature a specific review
    if len(manager.get_all_reviews()) > 0:
        review = manager.get_all_reviews()[0]
        manager.update_review(review['id'], is_featured=True)
        print(f"\n✅ Featured review from {review['author_name']}")
    
    manager.close()
    print()


def example_get_statistics():
    """Example: Getting and displaying review statistics"""
    print("📊 Example: Review Statistics\n")
    
    manager = ReviewManager()
    
    stats = manager.get_statistics()
    
    print(f"Total Reviews: {stats['total_reviews']}")
    print(f"Average Rating: {stats['average_rating']:.2f} / 5.0")
    print(f"\nRating Breakdown:")
    print(f"  ⭐⭐⭐⭐⭐ {stats['five_star_count']} ({stats['five_star_count']/max(stats['total_reviews'],1)*100:.1f}%)")
    print(f"  ⭐⭐⭐⭐   {stats['four_star_count']} ({stats['four_star_count']/max(stats['total_reviews'],1)*100:.1f}%)")
    print(f"  ⭐⭐⭐     {stats['three_star_count']} ({stats['three_star_count']/max(stats['total_reviews'],1)*100:.1f}%)")
    print(f"  ⭐⭐       {stats['two_star_count']} ({stats['two_star_count']/max(stats['total_reviews'],1)*100:.1f}%)")
    print(f"  ⭐         {stats['one_star_count']} ({stats['one_star_count']/max(stats['total_reviews'],1)*100:.1f}%)")
    
    manager.close()
    print()


def example_search_reviews():
    """Example: Searching for specific reviews"""
    print("🔍 Example: Searching Reviews\n")
    
    manager = ReviewManager()
    
    # Search for reviews containing "professional"
    results = manager.search_reviews("professional")
    print(f"Found {len(results)} reviews containing 'professional':")
    for review in results[:3]:  # Show first 3 results
        print(f"  - {review['author_name']}: \"{review['review_text'][:60]}...\"")
    
    manager.close()
    print()


def example_filter_by_rating():
    """Example: Getting reviews by rating"""
    print("⭐ Example: Filter Reviews by Rating\n")
    
    manager = ReviewManager()
    
    # Get all 5-star reviews
    five_star = manager.get_reviews_by_rating(5)
    print(f"5-Star Reviews: {len(five_star)}")
    
    # Get all 4-star reviews
    four_star = manager.get_reviews_by_rating(4)
    print(f"4-Star Reviews: {len(four_star)}")
    
    # Display some 5-star reviews
    if five_star:
        print(f"\nSample 5-star reviews:")
        for review in five_star[:2]:
            print(f"  - {review['author_name']}: \"{review['review_text'][:60]}...\"")
    
    manager.close()
    print()


def example_export_import():
    """Example: Exporting and importing reviews"""
    print("💾 Example: Export/Import Reviews\n")
    
    manager = ReviewManager()
    
    # Export all reviews to JSON
    export_path = manager.export_to_json('reviews_backup.json')
    print(f"✅ Exported all reviews to: {export_path}")
    
    # To import (uncomment to test):
    # manager.import_from_json('reviews_backup.json')
    # print("✅ Imported reviews from backup")
    
    manager.close()
    print()


def example_batch_operations():
    """Example: Batch operations on reviews"""
    print("📦 Example: Batch Operations\n")
    
    manager = ReviewManager()
    
    # Get all reviews
    all_reviews = manager.get_all_reviews()
    print(f"Total reviews in database: {len(all_reviews)}")
    
    # Update multiple reviews at once
    count = 0
    for review in all_reviews:
        if review['rating'] >= 5 and not review['is_featured']:
            manager.update_review(review['id'], is_featured=True)
            count += 1
            if count >= 3:  # Limit to 3 featured reviews
                break
    
    print(f"✅ Featured {count} top-rated reviews")
    
    # Get reviews from last 30 days (example logic)
    print("\nRecent reviews (last 30 days):")
    from datetime import datetime, timedelta
    recent_date = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
    recent_reviews = [r for r in all_reviews if r['review_date'] >= recent_date]
    print(f"  Found {len(recent_reviews)} recent reviews")
    
    manager.close()
    print()


def example_response_management():
    """Example: Managing business responses to reviews"""
    print("💬 Example: Managing Business Responses\n")
    
    manager = ReviewManager()
    
    # Get reviews without responses
    all_reviews = manager.get_all_reviews()
    no_response = [r for r in all_reviews if not r['response_text']]
    
    print(f"Reviews without response: {len(no_response)}")
    
    # Add response to a review
    if no_response:
        review = no_response[0]
        response = f"Thank you for your feedback, {review['author_name'].split()[0]}! We appreciate your business and are glad we could help with your move."
        
        manager.update_review(
            review['id'],
            response_text=response,
            response_date=datetime.now().strftime("%Y-%m-%d")
        )
        print(f"✅ Added response to review from {review['author_name']}")
    
    manager.close()
    print()


def main():
    """Run all examples"""
    print("\n" + "=" * 60)
    print("  OnTime Moving Review System - Usage Examples")
    print("=" * 60 + "\n")
    
    # Check if database exists and has data
    import os
    if not os.path.exists('reviews.db'):
        print("⚠️  Database not found. Please run setup first:")
        print("   python setup.py")
        print("   or")
        print("   python review_manager.py init\n")
        return
    
    # Run examples
    example_web_form_submission()
    example_add_reviews()
    example_feature_reviews()
    example_get_statistics()
    example_search_reviews()
    example_filter_by_rating()
    example_export_import()
    example_batch_operations()
    example_response_management()
    
    print("=" * 60)
    print("✅ All examples completed!")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()

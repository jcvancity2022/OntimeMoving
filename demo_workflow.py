"""
Demo: Complete Review Workflow
Demonstrates the full lifecycle of a review from submission to Google posting
"""

import time
from review_manager import ReviewManager
from google_reviews_helper import GoogleReviewsHelper


def print_header(text):
    """Print a formatted header"""
    print("\n" + "=" * 70)
    print(f"  {text}")
    print("=" * 70 + "\n")


def print_step(step_num, text):
    """Print a step in the workflow"""
    print(f"\n{'─' * 70}")
    print(f"STEP {step_num}: {text}")
    print('─' * 70 + "\n")


def demo_complete_workflow():
    """
    Demonstrate the complete workflow:
    1. Customer submits review on website
    2. Review is saved to database
    3. Admin reviews it
    4. Customer posts to Google
    5. Admin marks it as posted
    """
    
    print_header("🎬 OnTime Moving - Complete Review Workflow Demo")
    
    print("This demo simulates the entire review lifecycle from")
    print("customer submission to Google Reviews posting.\n")
    input("Press Enter to start the demo...")
    
    # Initialize managers
    manager = ReviewManager()
    helper = GoogleReviewsHelper()
    
    try:
        # STEP 1: Customer visits website and submits review
        print_step(1, "Customer Submits Review on Website")
        
        customer_data = {
            'author_name': 'Pardees Z',
            'rating': 5,
            'review_text': 'Ronald and his crew fantastic. They listened to our needs. The service was excellent and very thorough. Ronald came for an initial assessment and provided great tips on supplies etc for packing. He then returned 2 days prior to the move.',
        }
        
        print("📝 Customer fills out the web form:")
        print(f"   Name: {customer_data['author_name']}")
        print(f"   Rating: {'★' * customer_data['rating']}")
        print(f"   Review: \"{customer_data['review_text'][:60]}...\"")
        print("\n👆 Customer clicks 'Submit Review' button...")
        
        time.sleep(2)
        
        # Save to database (simulating API call)
        from datetime import datetime
        review_id = manager.add_review(
            author_name=customer_data['author_name'],
            rating=customer_data['rating'],
            review_text=customer_data['review_text'],
            review_date=datetime.now().strftime("%Y-%m-%d")
        )
        
        print(f"\n✅ Review saved to database (ID: {review_id})")
        print("📧 Admin notification sent")
        print("🌐 Customer sees: 'Thank you! Click below to also post on Google'")
        
        # STEP 2: Review appears in system
        print_step(2, "Review Appears in Admin Dashboard")
        
        print("Admin checks the dashboard:")
        time.sleep(1)
        
        summary = helper.get_review_summary()
        print(f"\n📊 Review Statistics:")
        print(f"   Total Reviews: {summary['total_reviews']}")
        print(f"   Average Rating: {summary['average_rating']} / 5.0")
        print(f"   Pending Google Post: {summary['pending_google_post']}")
        
        # Show the new review
        print(f"\n📋 New Review Details:")
        new_review = manager.get_review(review_id)
        print(f"   [{new_review['id']}] {new_review['author_name']}")
        print(f"   Rating: {'★' * new_review['rating']}")
        print(f"   Date: {new_review['review_date']}")
        print(f"   Featured: {'Yes' if new_review['is_featured'] else 'No'}")
        
        # STEP 3: Admin reviews and features it
        print_step(3, "Admin Reviews and Features the Review")
        
        print("Admin decides this is a great review and features it on homepage...")
        time.sleep(1)
        
        manager.update_review(review_id, is_featured=True)
        print(f"✅ Review '{review_id}' is now FEATURED")
        print("⭐ It will appear on the homepage in the 'Featured Reviews' section")
        
        # STEP 4: Check featured reviews
        print_step(4, "Featured Reviews Update")
        
        featured = manager.get_featured_reviews()
        print(f"Currently {len(featured)} featured reviews on homepage:\n")
        
        for rev in featured:
            print(f"   {'★' * rev['rating']} {rev['author_name']}")
            print(f"   \"{rev['review_text'][:50]}...\"")
            print()
        
        # STEP 5: Customer posts to Google
        print_step(5, "Customer Posts to Google Reviews")
        
        print("Customer clicked 'Post to Google Reviews' button on website")
        print("🌐 Google Reviews page opened in their browser")
        print("✍️  Customer copies their review and posts it to Google")
        print("\n(In real workflow, this happens in customer's browser)")
        
        input("\nPress Enter to simulate customer posting to Google...")
        
        print("\n✅ Customer successfully posted review to Google!")
        
        # STEP 6: Admin marks as posted to Google
        print_step(6, "Admin Marks Review as Posted to Google")
        
        print("Admin confirms the review is now on Google and marks it...")
        time.sleep(1)
        
        helper.mark_review_posted_to_google(review_id)
        print(f"✅ Review {review_id} marked as posted to Google")
        
        # Check updated status
        updated_review = manager.get_review(review_id)
        print(f"\n📝 Review Status:")
        print(f"   Response: {updated_review['response_text']}")
        
        # STEP 7: Final statistics
        print_step(7, "Updated Statistics")
        
        final_summary = helper.get_review_summary()
        print("📊 Final Dashboard:")
        print(f"   Total Reviews: {final_summary['total_reviews']}")
        print(f"   Average Rating: {final_summary['average_rating']} / 5.0")
        print(f"   Featured Reviews: {final_summary['featured_reviews']}")
        print(f"   Pending Google Post: {final_summary['pending_google_post']}")
        print(f"   Five-Star Rate: {final_summary['five_star_percentage']}%")
        
        # Summary
        print_header("✅ Workflow Complete!")
        
        print("Summary of what happened:\n")
        print("1. ✅ Customer submitted review on website")
        print("2. ✅ Review was saved to SQLite database")
        print("3. ✅ Admin reviewed and featured it")
        print("4. ✅ Featured review appeared on homepage")
        print("5. ✅ Customer posted to Google Reviews")
        print("6. ✅ Admin marked it as posted to Google")
        print("7. ✅ Dashboard statistics updated")
        
        print("\n🎉 The review is now:")
        print("   • Stored in your database")
        print("   • Featured on your website")
        print("   • Posted on Google Reviews")
        print("   • Tracked in your system")
        
    finally:
        manager.close()
        helper.close()
    
    print("\n" + "=" * 70 + "\n")


def demo_quick_workflow():
    """Quick demonstration of key features"""
    print_header("⚡ Quick Feature Demo")
    
    helper = GoogleReviewsHelper()
    
    print("1. Dashboard")
    print("─" * 70)
    helper.display_review_dashboard()
    
    print("\n2. Pending Reviews")
    print("─" * 70)
    pending = helper.get_pending_reviews()
    print(f"Found {len(pending)} reviews waiting to be posted to Google\n")
    
    for rev in pending[:3]:  # Show first 3
        print(f"   [{rev['id']}] {rev['author_name']} - {'★' * rev['rating']}")
    
    print("\n3. Recent Reviews")
    print("─" * 70)
    manager = ReviewManager()
    recent = manager.get_all_reviews(limit=5)
    print(f"Last 5 reviews:\n")
    
    for rev in recent:
        print(f"   {rev['review_date']} | {rev['author_name']} | {'★' * rev['rating']}")
    
    manager.close()
    helper.close()
    
    print("\n" + "=" * 70 + "\n")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "quick":
        demo_quick_workflow()
    else:
        demo_complete_workflow()

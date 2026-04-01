"""
Test script for OnTime Moving Review System
Validates database operations and API functionality
"""

import sys
from review_manager import ReviewManager


def test_database_operations():
    """Test database CRUD operations"""
    print("🧪 Testing Database Operations\n")
    
    try:
        manager = ReviewManager('test_reviews.db')
        print("✅ Database connection established")
        
        # Test: Add review
        print("\n📝 Test: Adding review...")
        review_id = manager.add_review(
            author_name="Xiying Li",
            rating=5,
            review_text="This is a test review",
            is_featured=True
        )
        print(f"✅ Review added with ID: {review_id}")
        
        # Test: Get review
        print("\n📖 Test: Retrieving review...")
        review = manager.get_review(review_id)
        assert review is not None, "Review not found"
        assert review['author_name'] == "Xiying Li", "Author name mismatch"
        assert review['rating'] == 5, "Rating mismatch"
        print(f"✅ Review retrieved: {review['author_name']} - {review['rating']} stars")
        
        # Test: Update review
        print("\n✏️ Test: Updating review...")
        manager.update_review(review_id, rating=4, is_featured=False)
        updated_review = manager.get_review(review_id)
        assert updated_review['rating'] == 4, "Rating not updated"
        assert updated_review['is_featured'] == 0, "Featured flag not updated"
        print("✅ Review updated successfully")
        
        # Test: Get all reviews
        print("\n📚 Test: Getting all reviews...")
        all_reviews = manager.get_all_reviews()
        assert len(all_reviews) > 0, "No reviews found"
        print(f"✅ Found {len(all_reviews)} reviews")
        
        # Test: Get featured reviews
        print("\n⭐ Test: Getting featured reviews...")
        featured = manager.get_featured_reviews()
        print(f"✅ Found {len(featured)} featured reviews")
        
        # Test: Statistics
        print("\n📊 Test: Getting statistics...")
        stats = manager.get_statistics()
        assert stats['total_reviews'] > 0, "No reviews in statistics"
        print(f"✅ Statistics: {stats['total_reviews']} reviews, avg rating: {stats['average_rating']:.1f}")
        
        # Test: Search
        print("\n🔍 Test: Searching reviews...")
        results = manager.search_reviews("test")
        assert len(results) > 0, "Search returned no results"
        print(f"✅ Search found {len(results)} results")
        
        # Test: Export
        print("\n💾 Test: Exporting to JSON...")
        export_path = manager.export_to_json('test_export.json')
        print(f"✅ Exported to {export_path}")
        
        # Test: Delete review
        print("\n🗑️ Test: Deleting review...")
        manager.delete_review(review_id)
        deleted_review = manager.get_review(review_id)
        assert deleted_review is None, "Review still exists after deletion"
        print("✅ Review deleted successfully")
        
        manager.close()
        
        # Clean up test files
        import os
        if os.path.exists('test_reviews.db'):
            os.remove('test_reviews.db')
        if os.path.exists('test_export.json'):
            os.remove('test_export.json')
        
        print("\n" + "=" * 50)
        print("✅ All database tests passed!")
        print("=" * 50 + "\n")
        return True
        
    except AssertionError as e:
        print(f"\n❌ Test failed: {e}")
        return False
    except Exception as e:
        print(f"\n❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_api_endpoints():
    """Test API endpoints (requires server to be running)"""
    print("🧪 Testing API Endpoints\n")
    
    try:
        import requests
        
        base_url = "http://localhost:5000/api"
        
        # Test: Get reviews
        print("📡 Test: GET /api/reviews...")
        response = requests.get(f"{base_url}/reviews", timeout=5)
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        assert data['success'] == True, "API returned failure"
        print(f"✅ Got {data['count']} reviews")
        
        # Test: Get statistics
        print("\n📡 Test: GET /api/statistics...")
        response = requests.get(f"{base_url}/statistics", timeout=5)
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        assert data['success'] == True, "API returned failure"
        print(f"✅ Average rating: {data['statistics']['average_rating']:.1f}")
        
        print("\n" + "=" * 50)
        print("✅ All API tests passed!")
        print("=" * 50 + "\n")
        return True
        
    except ImportError:
        print("⚠️  'requests' library not installed. Skipping API tests.")
        print("   Install with: pip install requests")
        return True
    except requests.exceptions.ConnectionError:
        print("⚠️  Cannot connect to API server at http://localhost:5000")
        print("   Start the server with: python api_server.py")
        return True
    except Exception as e:
        print(f"\n❌ API test failed: {e}")
        return False


def main():
    """Run all tests"""
    print("\n" + "=" * 50)
    print("  OnTime Moving Review System - Test Suite")
    print("=" * 50 + "\n")
    
    success = True
    
    # Run database tests
    if not test_database_operations():
        success = False
    
    # Run API tests
    print("\n")
    if not test_api_endpoints():
        success = False
    
    if success:
        print("\n🎉 All tests completed successfully!")
        return 0
    else:
        print("\n⚠️  Some tests failed. Please review the output above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())

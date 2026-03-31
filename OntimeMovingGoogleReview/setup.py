"""
Setup script for OnTime Moving Review System
Automatically installs dependencies and initializes the database
"""

import subprocess
import sys
import os


def print_header(text):
    """Print a formatted header"""
    print("\n" + "=" * 60)
    print(f"  {text}")
    print("=" * 60 + "\n")


def check_python_version():
    """Check if Python version is compatible"""
    print("🔍 Checking Python version...")
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 7):
        print("❌ Python 3.7 or higher is required")
        print(f"   Current version: {version.major}.{version.minor}.{version.micro}")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} detected")
    return True


def install_dependencies():
    """Install required Python packages"""
    print_header("Installing Dependencies")
    
    try:
        print("📦 Installing packages from requirements.txt...")
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "-r", "requirements.txt", "-q"
        ])
        print("✅ All dependencies installed successfully\n")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False


def initialize_database():
    """Initialize the database with sample data"""
    print_header("Initializing Database")
    
    try:
        # Check if database already exists
        if os.path.exists('reviews.db'):
            response = input("⚠️  Database already exists. Overwrite? (y/N): ")
            if response.lower() != 'y':
                print("ℹ️  Skipping database initialization")
                return True
            os.remove('reviews.db')
            print("🗑️  Removed existing database")
        
        print("📊 Creating database and adding sample reviews...")
        from review_manager import initialize_with_sample_data
        initialize_with_sample_data()
        print("✅ Database initialized successfully\n")
        return True
    except Exception as e:
        print(f"❌ Failed to initialize database: {e}")
        return False


def test_api_server():
    """Test if the API server can be imported"""
    print_header("Testing API Server")
    
    try:
        print("🧪 Checking API server...")
        import api_server
        print("✅ API server module loaded successfully\n")
        return True
    except Exception as e:
        print(f"❌ Failed to load API server: {e}")
        return False


def display_next_steps():
    """Display next steps for the user"""
    print_header("Setup Complete!")
    
    print("🎉 Your OnTime Moving Review System is ready!\n")
    print("📋 Next Steps:\n")
    print("1️⃣  Start the API server:")
    print("   python api_server.py\n")
    print("2️⃣  Open index.html in your browser")
    print("   - For static mode: just open the file")
    print("   - For dynamic mode: add data-dynamic-reviews=\"true\" to <body> tag\n")
    print("3️⃣  Access the API at:")
    print("   http://localhost:5000/api/reviews\n")
    print("📚 For more information, see README.md\n")
    print("=" * 60)


def main():
    """Main setup function"""
    print_header("OnTime Moving Review System Setup")
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        print("\n⚠️  Setup incomplete. Please install dependencies manually:")
        print("   pip install -r requirements.txt")
        sys.exit(1)
    
    # Initialize database
    if not initialize_database():
        print("\n⚠️  Database initialization failed. You can try manually:")
        print("   python review_manager.py init")
        sys.exit(1)
    
    # Test API server
    if not test_api_server():
        print("\n⚠️  API server test failed, but you can still proceed.")
    
    # Display next steps
    display_next_steps()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Setup interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)

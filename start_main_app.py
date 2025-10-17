#!/usr/bin/env python3
"""
Script to start the main Django application
"""
import subprocess
import sys
import os
from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).parent

def main():
    """Start the main Django application"""
    print("🚀 Starting SvoiCode Main Application...")
    print("=" * 50)
    
    # Change to base directory
    os.chdir(BASE_DIR)
    
    # Check if virtual environment exists
    venv_path = BASE_DIR / 'venv'
    if venv_path.exists():
        print("✅ Virtual environment found")
        
        # Activate virtual environment and run Django
        if sys.platform == "win32":
            activate_script = venv_path / 'Scripts' / 'activate.bat'
            command = f'"{activate_script}" && python manage.py runserver 0.0.0.0:8000'
        else:
            activate_script = venv_path / 'bin' / 'activate'
            command = f'source "{activate_script}" && python manage.py runserver 0.0.0.0:8000'
        
        print("🌐 Starting Django server on http://localhost:8000")
        print("📱 Make sure microservices are running for full functionality")
        print("\nPress Ctrl+C to stop the server...")
        
        try:
            subprocess.run(command, shell=True, check=True)
        except KeyboardInterrupt:
            print("\n🛑 Server stopped")
        except subprocess.CalledProcessError as e:
            print(f"❌ Error starting server: {e}")
    else:
        print("❌ Virtual environment not found. Please create one first:")
        print("   python -m venv venv")
        print("   venv\\Scripts\\activate  # Windows")
        print("   source venv/bin/activate  # Linux/Mac")
        print("   pip install -r requirements.txt")

if __name__ == "__main__":
    main()

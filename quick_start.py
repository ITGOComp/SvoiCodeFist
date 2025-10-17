#!/usr/bin/env python
"""
Quick start script for SvoiCode project
"""
import os
import sys
import subprocess

def check_django_setup():
    """Check if Django is properly set up"""
    try:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SvoiCode.settings')
        import django
        django.setup()
        
        from django.conf import settings
        print(f"✅ Django settings loaded successfully")
        print(f"   DEBUG: {settings.DEBUG}")
        print(f"   USE_MICROSERVICES: {getattr(settings, 'USE_MICROSERVICES', 'Not set')}")
        print(f"   ALLOWED_HOSTS: {settings.ALLOWED_HOSTS}")
        
        return True
    except Exception as e:
        print(f"❌ Django setup error: {e}")
        return False

def run_migrations():
    """Run Django migrations"""
    try:
        print("🔄 Running migrations...")
        result = subprocess.run([sys.executable, 'manage.py', 'migrate'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Migrations completed successfully")
            return True
        else:
            print(f"❌ Migration error: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Error running migrations: {e}")
        return False

def start_server():
    """Start Django development server"""
    try:
        print("🚀 Starting Django development server...")
        print("📍 Server will be available at: http://localhost:8000")
        print("🛑 Press Ctrl+C to stop the server")
        print("=" * 50)
        
        subprocess.run([sys.executable, 'manage.py', 'runserver'])
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except Exception as e:
        print(f"❌ Error starting server: {e}")

def main():
    """Main function"""
    print("🚀 SvoiCode Quick Start")
    print("=" * 30)
    
    # Check Django setup
    if not check_django_setup():
        print("❌ Django setup failed. Please check your configuration.")
        return False
    
    # Run migrations
    if not run_migrations():
        print("❌ Migrations failed. Please check your database configuration.")
        return False
    
    # Start server
    start_server()
    
    return True

if __name__ == "__main__":
    main()

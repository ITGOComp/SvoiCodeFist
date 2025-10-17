#!/usr/bin/env python
"""
Quick fix script for Django settings
"""
import os
import sys

def fix_allowed_hosts():
    """Fix ALLOWED_HOSTS in settings.py"""
    settings_file = os.path.join(os.path.dirname(__file__), 'SvoiCode', 'settings.py')
    
    try:
        with open(settings_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if localhost is already in ALLOWED_HOSTS
        if 'localhost' in content and 'ALLOWED_HOSTS' in content:
            print("✅ ALLOWED_HOSTS already includes localhost")
            return True
        
        # Add localhost to ALLOWED_HOSTS
        import re
        pattern = r"ALLOWED_HOSTS\s*=\s*\[(.*?)\]"
        match = re.search(pattern, content, re.DOTALL)
        
        if match:
            current_hosts = match.group(1)
            new_hosts = current_hosts.rstrip().rstrip(',') + ",\n    'localhost',\n    'localhost:8000',\n    'localhost:9000',\n    '127.0.0.1:8000',\n    '127.0.0.1:9000'"
            new_content = content.replace(match.group(0), f"ALLOWED_HOSTS = [{new_hosts}]")
            
            with open(settings_file, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            print("✅ Fixed ALLOWED_HOSTS in settings.py")
            return True
        else:
            print("❌ Could not find ALLOWED_HOSTS in settings.py")
            return False
            
    except Exception as e:
        print(f"❌ Error fixing settings: {e}")
        return False

def check_django_setup():
    """Check if Django is properly set up"""
    try:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SvoiCode.settings')
        import django
        django.setup()
        
        from django.conf import settings
        print(f"✅ Django settings loaded successfully")
        print(f"   ALLOWED_HOSTS: {settings.ALLOWED_HOSTS}")
        print(f"   DEBUG: {settings.DEBUG}")
        print(f"   USE_MICROSERVICES: {getattr(settings, 'USE_MICROSERVICES', 'Not set')}")
        
        return True
    except Exception as e:
        print(f"❌ Django setup error: {e}")
        return False

def main():
    """Main function"""
    print("🔧 Fixing Django settings...")
    
    # Fix ALLOWED_HOSTS
    if fix_allowed_hosts():
        print("✅ Settings fixed successfully")
    else:
        print("❌ Failed to fix settings")
        return False
    
    # Check Django setup
    if check_django_setup():
        print("✅ Django is properly configured")
    else:
        print("❌ Django configuration issues")
        return False
    
    print("\n🎉 All fixes applied successfully!")
    print("You can now run: python manage.py runserver")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

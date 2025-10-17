#!/usr/bin/env python
"""
Test script to verify website is working
"""
import os
import sys
import requests
import time

def test_website():
    """Test if website is accessible"""
    base_url = "http://localhost:8000"
    
    print("🧪 Testing website accessibility...")
    
    try:
        # Test main page
        print("📄 Testing main page...")
        response = requests.get(base_url, timeout=10)
        
        if response.status_code == 200:
            print("✅ Main page is accessible")
            
            # Check if it's HTML (not JSON)
            content_type = response.headers.get('content-type', '')
            if 'text/html' in content_type:
                print("✅ Response is HTML (not JSON)")
                
                # Check if it contains expected content
                content = response.text
                if 'ЦОДД' in content or 'SvoiCode' in content:
                    print("✅ Page contains expected content")
                    return True
                else:
                    print("⚠️  Page content seems unexpected")
                    return False
            else:
                print(f"❌ Response is not HTML: {content_type}")
                return False
        else:
            print(f"❌ Main page returned status {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to localhost:8000")
        print("   Make sure Django server is running: python manage.py runserver")
        return False
    except requests.exceptions.Timeout:
        print("❌ Request timed out")
        return False
    except Exception as e:
        print(f"❌ Error testing website: {e}")
        return False

def test_api_endpoints():
    """Test API endpoints"""
    base_url = "http://localhost:8000"
    
    print("\n🔌 Testing API endpoints...")
    
    endpoints = [
        "/api/incidents/",
        "/api/traffic/",
        "/api/patrols/",
        "/api/cameras/",
        "/api/detectors/",
    ]
    
    results = {}
    
    for endpoint in endpoints:
        try:
            response = requests.get(f"{base_url}{endpoint}", timeout=5)
            if response.status_code == 200:
                results[endpoint] = "✅ OK"
            else:
                results[endpoint] = f"❌ HTTP {response.status_code}"
        except Exception as e:
            results[endpoint] = f"❌ Error: {str(e)[:30]}..."
    
    for endpoint, status in results.items():
        print(f"  {status} {endpoint}")
    
    success_count = sum(1 for status in results.values() if status.startswith("✅"))
    print(f"\n📊 API Summary: {success_count}/{len(results)} endpoints working")
    
    return success_count > 0

def main():
    """Main test function"""
    print("🚀 SvoiCode Website Test")
    print("=" * 30)
    
    # Test main website
    website_ok = test_website()
    
    # Test API endpoints
    api_ok = test_api_endpoints()
    
    print("\n" + "=" * 30)
    print("🏁 TEST RESULTS")
    print("=" * 30)
    
    if website_ok:
        print("✅ Website is working correctly!")
        print("🌐 Open http://localhost:8000 in your browser")
    else:
        print("❌ Website has issues")
        print("🔧 Try running: python manage.py runserver")
    
    if api_ok:
        print("✅ API endpoints are working")
    else:
        print("⚠️  Some API endpoints may have issues")
    
    if website_ok and api_ok:
        print("\n🎉 Everything is working perfectly!")
        return True
    else:
        print("\n⚠️  Some issues detected. Check the output above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

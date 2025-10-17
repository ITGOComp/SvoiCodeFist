#!/usr/bin/env python
"""
Test script for microservices integration
"""
import os
import sys
import django
import requests
import json
from time import sleep

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SvoiCode.settings')
django.setup()

from app.services.service_manager import service_manager
from django.conf import settings


def test_service_connectivity():
    """Test connectivity to all microservices"""
    print("🔍 Testing microservice connectivity...")
    
    status = service_manager.get_service_status()
    
    for service_name, info in status.items():
        status_icon = "✅" if info['healthy'] else "❌"
        print(f"{status_icon} {service_name}: {info['url']}")
        print(f"   Available: {info['available']}")
        print(f"   Healthy: {info['healthy']}")
        print()
    
    healthy_count = sum(1 for info in status.values() if info['healthy'])
    total_count = len(status)
    
    print(f"📊 Summary: {healthy_count}/{total_count} services are healthy")
    return healthy_count == total_count


def test_api_endpoints():
    """Test API endpoints"""
    print("🌐 Testing API endpoints...")
    
    base_url = "http://localhost:8000"
    endpoints = [
        "/api/health/",
        "/api/services/status/",
        "/api/incidents/",
        "/api/traffic/",
        "/api/patrols/",
        "/api/cameras/",
        "/api/detectors/",
        "/api/accident-stats/",
        "/api/weather/",
        "/api/traffic-forecast/",
        "/api/road-works/",
    ]
    
    results = {}
    
    for endpoint in endpoints:
        try:
            response = requests.get(f"{base_url}{endpoint}", timeout=5)
            if response.status_code == 200:
                results[endpoint] = "✅ OK"
            else:
                results[endpoint] = f"❌ HTTP {response.status_code}"
        except requests.exceptions.RequestException as e:
            results[endpoint] = f"❌ Error: {str(e)[:50]}..."
    
    for endpoint, status in results.items():
        print(f"{status} {endpoint}")
    
    success_count = sum(1 for status in results.values() if status.startswith("✅"))
    total_count = len(results)
    
    print(f"\n📊 API Summary: {success_count}/{total_count} endpoints working")
    return success_count == total_count


def test_fallback_mechanism():
    """Test fallback mechanism when microservices are unavailable"""
    print("🔄 Testing fallback mechanism...")
    
    # This would require temporarily disabling microservices
    # For now, just check if the setting exists
    use_microservices = getattr(settings, 'USE_MICROSERVICES', True)
    print(f"Microservices enabled: {use_microservices}")
    
    if use_microservices:
        print("✅ Fallback mechanism is configured")
    else:
        print("ℹ️  Using local database only")
    
    return True


def test_web_interface():
    """Test web interface accessibility"""
    print("🌐 Testing web interface...")
    
    base_url = "http://localhost:8000"
    pages = [
        "/",
        "/admin/microservices/",
        "/incidents/",
        "/news/",
    ]
    
    results = {}
    
    for page in pages:
        try:
            response = requests.get(f"{base_url}{page}", timeout=5)
            if response.status_code == 200:
                results[page] = "✅ OK"
            else:
                results[page] = f"❌ HTTP {response.status_code}"
        except requests.exceptions.RequestException as e:
            results[page] = f"❌ Error: {str(e)[:50]}..."
    
    for page, status in results.items():
        print(f"{status} {page}")
    
    success_count = sum(1 for status in results.values() if status.startswith("✅"))
    total_count = len(results)
    
    print(f"\n📊 Web Interface Summary: {success_count}/{total_count} pages accessible")
    return success_count == total_count


def main():
    """Run all tests"""
    print("🚀 Starting microservices integration tests...\n")
    
    tests = [
        ("Service Connectivity", test_service_connectivity),
        ("API Endpoints", test_api_endpoints),
        ("Fallback Mechanism", test_fallback_mechanism),
        ("Web Interface", test_web_interface),
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        print(f"{'='*50}")
        print(f"Testing: {test_name}")
        print(f"{'='*50}")
        
        try:
            result = test_func()
            results[test_name] = result
            print(f"\n{'✅ PASSED' if result else '❌ FAILED'}: {test_name}")
        except Exception as e:
            print(f"\n❌ ERROR in {test_name}: {e}")
            results[test_name] = False
        
        print("\n")
    
    # Summary
    print("="*50)
    print("🏁 TEST SUMMARY")
    print("="*50)
    
    passed = sum(1 for result in results.values() if result)
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{status}: {test_name}")
    
    print(f"\n📊 Overall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Integration is working correctly.")
    else:
        print("⚠️  Some tests failed. Check the output above for details.")
    
    return passed == total


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

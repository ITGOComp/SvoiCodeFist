#!/usr/bin/env python3
"""
Script to check the status of all microservices
"""
import requests
import time
from pathlib import Path

# Service configurations
SERVICES = {
    'user_service': 8001,
    'incident_service': 8002,
    'traffic_service': 8003,
    'news_service': 8004,
    'chat_service': 8005,
    'analytics_service': 8006,
    'traffic_analytics_service': 8007,
    'schedule_service': 8008,
    'notification_service': 8009,
    'api_gateway': 9000,
    'main_app': 8000
}

def check_service(service_name, port):
    """Check if a service is responding"""
    try:
        # Try health endpoint first
        response = requests.get(f'http://localhost:{port}/health', timeout=2)
        if response.status_code == 200:
            return True, "Healthy"
    except:
        pass
    
    try:
        # Try root endpoint
        response = requests.get(f'http://localhost:{port}/', timeout=2)
        if response.status_code in [200, 404]:  # 404 is ok for root endpoint
            return True, "Running"
    except:
        pass
    
    return False, "Not responding"

def main():
    """Check all services"""
    print("🔍 Checking SvoiCode Services Status...")
    print("=" * 60)
    
    healthy_count = 0
    total_count = len(SERVICES)
    
    for service_name, port in SERVICES.items():
        is_healthy, status = check_service(service_name, port)
        
        if is_healthy:
            print(f"✅ {service_name:<25} :{port:<5} - {status}")
            healthy_count += 1
        else:
            print(f"❌ {service_name:<25} :{port:<5} - {status}")
    
    print("=" * 60)
    print(f"📊 Status: {healthy_count}/{total_count} services running")
    
    if healthy_count == total_count:
        print("🎉 All services are running!")
    elif healthy_count > 0:
        print("⚠️  Some services are not running")
    else:
        print("❌ No services are running")
    
    print("\n💡 To start all services, run: python start_microservices.py")
    print("💡 To start main app, run: python start_main_app.py")

if __name__ == "__main__":
    main()

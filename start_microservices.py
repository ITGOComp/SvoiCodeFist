#!/usr/bin/env python3
"""
Script to start all microservices
"""
import subprocess
import time
import sys
import os
import signal
from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).parent

# Service configurations
SERVICES = {
    'user_service': {
        'port': 8001,
        'path': 'services/user_service',
        'command': ['python', 'manage.py', 'runserver', '0.0.0.0:8001']
    },
    'incident_service': {
        'port': 8002,
        'path': 'services/incident_service',
        'command': ['python', 'manage.py', 'runserver', '0.0.0.0:8002']
    },
    'traffic_service': {
        'port': 8003,
        'path': 'services/traffic_service',
        'command': ['python', 'manage.py', 'runserver', '0.0.0.0:8003']
    },
    'news_service': {
        'port': 8004,
        'path': 'services/news_service',
        'command': ['python', 'manage.py', 'runserver', '0.0.0.0:8004']
    },
    'chat_service': {
        'port': 8005,
        'path': 'services/chat_service',
        'command': ['python', 'manage.py', 'runserver', '0.0.0.0:8005']
    },
    'analytics_service': {
        'port': 8006,
        'path': 'services/analytics_service',
        'command': ['python', 'manage.py', 'runserver', '0.0.0.0:8006']
    },
    'traffic_analytics_service': {
        'port': 8007,
        'path': 'services/traffic_analytics_service',
        'command': ['python', 'manage.py', 'runserver', '0.0.0.0:8007']
    },
    'schedule_service': {
        'port': 8008,
        'path': 'services/schedule_service',
        'command': ['python', 'manage.py', 'runserver', '0.0.0.0:8008']
    },
    'notification_service': {
        'port': 8009,
        'path': 'services/notification_service',
        'command': ['python', 'manage.py', 'runserver', '0.0.0.0:8009']
    },
    'api_gateway': {
        'port': 9000,
        'path': 'services/api_gateway',
        'command': ['python', 'main.py']
    }
}

# Store process references
processes = {}

def start_service(service_name, config):
    """Start a single service"""
    service_path = BASE_DIR / config['path']
    
    if not service_path.exists():
        print(f"❌ Service path not found: {service_path}")
        return None
    
    print(f"🚀 Starting {service_name} on port {config['port']}...")
    
    try:
        # Change to service directory
        os.chdir(service_path)
        
        # Start the service
        process = subprocess.Popen(
            config['command'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Store process reference
        processes[service_name] = process
        
        print(f"✅ {service_name} started with PID {process.pid}")
        return process
        
    except Exception as e:
        print(f"❌ Failed to start {service_name}: {e}")
        return None
    finally:
        # Return to base directory
        os.chdir(BASE_DIR)

def stop_all_services():
    """Stop all running services"""
    print("\n🛑 Stopping all services...")
    
    for service_name, process in processes.items():
        if process and process.poll() is None:
            print(f"🛑 Stopping {service_name}...")
            try:
                process.terminate()
                process.wait(timeout=5)
                print(f"✅ {service_name} stopped")
            except subprocess.TimeoutExpired:
                print(f"⚠️  Force killing {service_name}...")
                process.kill()
                process.wait()
                print(f"✅ {service_name} force stopped")
            except Exception as e:
                print(f"❌ Error stopping {service_name}: {e}")

def check_service_health(service_name, port):
    """Check if service is responding"""
    import requests
    try:
        response = requests.get(f'http://localhost:{port}/health', timeout=2)
        return response.status_code == 200
    except:
        return False

def main():
    """Main function"""
    print("🚀 Starting SvoiCode Microservices...")
    print("=" * 50)
    
    # Start all services
    for service_name, config in SERVICES.items():
        start_service(service_name, config)
        time.sleep(2)  # Give each service time to start
    
    print("\n" + "=" * 50)
    print("🔍 Checking service health...")
    
    # Check health of services
    for service_name, config in SERVICES.items():
        if check_service_health(service_name, config['port']):
            print(f"✅ {service_name} is healthy")
        else:
            print(f"⚠️  {service_name} may not be ready yet")
    
    print("\n" + "=" * 50)
    print("🎉 All services started!")
    print("📱 Main website: http://localhost:8000")
    print("🔧 API Gateway: http://localhost:9000")
    print("\nPress Ctrl+C to stop all services...")
    
    # Set up signal handler for graceful shutdown
    def signal_handler(sig, frame):
        print(f"\n🛑 Received signal {sig}")
        stop_all_services()
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Keep the script running
    try:
        while True:
            time.sleep(1)
            
            # Check if any process died
            for service_name, process in list(processes.items()):
                if process and process.poll() is not None:
                    print(f"⚠️  {service_name} has stopped unexpectedly")
                    del processes[service_name]
                    
    except KeyboardInterrupt:
        print("\n🛑 Shutting down...")
        stop_all_services()

if __name__ == "__main__":
    main()

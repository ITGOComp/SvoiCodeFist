#!/usr/bin/env python3
"""
Script to start everything - microservices and main app
"""
import subprocess
import time
import threading
import sys
from pathlib import Path

def run_microservices():
    """Run microservices in background"""
    print("🚀 Starting microservices...")
    subprocess.run([sys.executable, "start_microservices.py"])

def run_main_app():
    """Run main Django app"""
    print("🌐 Starting main Django app...")
    subprocess.run([sys.executable, "start_main_app.py"])

def main():
    """Start everything"""
    print("🚀 Starting SvoiCode Full Stack...")
    print("=" * 50)
    
    # Start microservices in background thread
    microservices_thread = threading.Thread(target=run_microservices, daemon=True)
    microservices_thread.start()
    
    # Wait a bit for microservices to start
    print("⏳ Waiting for microservices to start...")
    time.sleep(10)
    
    # Start main app (this will block)
    run_main_app()

if __name__ == "__main__":
    main()

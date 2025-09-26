#!/usr/bin/env python3
"""
Script to run both FastAPI backend and Taipy frontend
"""
import subprocess
import sys
import time
import os

def run_fastapi():
    """Start FastAPI backend"""
    print("🚀 Starting FastAPI backend on port 8000...")
    os.chdir("app")
    return subprocess.Popen([
        sys.executable, "main.py"
    ])

def run_taipy():
    """Start Taipy frontend"""
    print("🎨 Starting Taipy frontend on port 5000...")
    time.sleep(3)  # Give FastAPI time to start
    os.chdir("..")  # Go back to root directory
    return subprocess.Popen([
        sys.executable, "taipy_frontend.py"
    ])

if __name__ == "__main__":
    try:
        # Start FastAPI backend
        fastapi_process = run_fastapi()
        
        # Start Taipy frontend
        taipy_process = run_taipy()
        
        print("\n" + "="*50)
        print("🎉 Both services are running!")
        print("📡 FastAPI Backend: http://localhost:8000")
        print("🌐 Taipy Frontend: http://localhost:5000")
        print("="*50)
        print("\nPress Ctrl+C to stop both services")
        
        # Wait for processes
        fastapi_process.wait()
        taipy_process.wait()
        
    except KeyboardInterrupt:
        print("\n🛑 Stopping services...")
        if 'fastapi_process' in locals():
            fastapi_process.terminate()
        if 'taipy_process' in locals():
            taipy_process.terminate()
        print("✅ Services stopped")
#!/usr/bin/env python3
"""
Launcher for The Quiet Water of Cabeus
Run this file to start backend + open browser
"""
import subprocess
import sys
import time
import webbrowser
import os
import signal
import threading

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
VENV_PYTHON = os.path.join(BASE_DIR, ".venv", "Scripts", "python.exe")

def run_backend():
    """Run uvicorn backend"""
    cmd = [VENV_PYTHON, "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
    return subprocess.Popen(cmd, cwd=BASE_DIR)

def wait_for_server(url, timeout=30):
    """Wait for server to be ready"""
    import urllib.request
    start = time.time()
    while time.time() - start < timeout:
        try:
            urllib.request.urlopen(url, timeout=2)
            return True
        except:
            time.sleep(0.5)
    return False

def main():
    print("=" * 50)
    print("The Quiet Water of Cabeus - Launcher")
    print("=" * 50)
    
    # Start backend
    print("\n[1/3] Starting backend server...")
    backend = run_backend()
    
    # Wait for server
    print("[2/3] Waiting for server to be ready...")
    if wait_for_server("http://localhost:8000/"):
        print("      Server ready!")
    else:
        print("      ERROR: Server didn't start in time")
        backend.terminate()
        return 1
    
    # Open browser
    print("[3/3] Opening browser...")
    webbrowser.open("http://localhost:8000/")
    
    print("\n" + "=" * 50)
    print("Running at: http://localhost:8000/")
    print("API docs:   http://localhost:8000/api")
    print("Events:     http://localhost:8000/api/events")
    print("=" * 50)
    print("\nPress Ctrl+C to stop...")
    
    try:
        backend.wait()
    except KeyboardInterrupt:
        print("\n\nShutting down...")
        backend.terminate()
        backend.wait(timeout=5)
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
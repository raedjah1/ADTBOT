"""
SmartWebBot Desktop App Launcher - Windows Compatible Version
"""

import os
import sys
import time
import subprocess
import threading
from pathlib import Path

def check_node_installed():
    """Check if Node.js is installed."""
    try:
        result = subprocess.run(['node', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            version = result.stdout.strip()
            print(f"[OK] Node.js found: {version}")
            return True
        else:
            print("[ERROR] Node.js not found")
            return False
    except FileNotFoundError:
        print("[ERROR] Node.js not found")
        return False

def install_frontend_dependencies():
    """Install frontend dependencies."""
    frontend_dir = Path("frontend")
    
    if not frontend_dir.exists():
        print("[ERROR] Frontend directory not found")
        return False
    
    # Check if node_modules already exists
    if (frontend_dir / "node_modules").exists():
        print("[OK] Frontend dependencies already installed")
        return True
    
    print("[INFO] Installing frontend dependencies...")
    
    try:
        result = subprocess.run(
            ['npm', 'install', '--legacy-peer-deps'], 
            cwd=frontend_dir,
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print("[OK] Frontend dependencies installed successfully")
            return True
        else:
            print(f"[ERROR] Failed to install dependencies: {result.stderr}")
            return False
            
    except FileNotFoundError:
        print("[ERROR] npm not found. Please install Node.js")
        return False

def start_backend():
    """Start the Python backend server."""
    print("[INFO] Starting Python backend server...")
    
    try:
        subprocess.run([sys.executable, 'backend_server.py'])
    except KeyboardInterrupt:
        print("\n[INFO] Backend server stopped")
    except Exception as e:
        print(f"[ERROR] Failed to start backend: {e}")

def start_frontend():
    """Start the Electron frontend."""
    print("[INFO] Starting Electron frontend...")
    
    frontend_dir = Path("frontend")
    
    try:
        subprocess.run(['npm', 'run', 'electron-dev'], cwd=frontend_dir)
    except KeyboardInterrupt:
        print("\n[INFO] Frontend stopped")
    except Exception as e:
        print(f"[ERROR] Failed to start frontend: {e}")

def main():
    """Main launcher function."""
    print("SmartWebBot Desktop App Launcher")
    print("=" * 50)
    
    # Check Node.js
    if not check_node_installed():
        print("\n[INFO] Please install Node.js from: https://nodejs.org/")
        print("   Then run this script again.")
        return
    
    # Install frontend dependencies
    if not install_frontend_dependencies():
        print("\n[ERROR] Failed to set up frontend dependencies")
        return
    
    print("\n[OK] Setup complete! Choose how to run the app:")
    print("1. Full Desktop App (Electron + Python backend)")
    print("2. Backend Only (for development)")
    print("3. Frontend Only (requires backend running separately)")
    
    choice = input("\nEnter your choice (1-3): ").strip()
    
    if choice == "1":
        print("\n[INFO] Starting Full Desktop App...")
        print("[INFO] Backend will start at: http://localhost:8000")
        print("[INFO] Frontend will open automatically")
        print("[INFO] Press Ctrl+C to stop both services\n")
        
        # Start backend in a separate thread
        backend_thread = threading.Thread(target=start_backend, daemon=True)
        backend_thread.start()
        
        # Give backend time to start
        time.sleep(3)
        
        # Start frontend (this will block)
        start_frontend()
        
    elif choice == "2":
        print("\n[INFO] Starting Backend Only...")
        print("[INFO] API will be available at: http://localhost:8000")
        print("[INFO] API docs at: http://localhost:8000/docs")
        print("[INFO] Press Ctrl+C to stop\n")
        
        start_backend()
        
    elif choice == "3":
        print("\n[INFO] Starting Frontend Only...")
        print("[INFO] Make sure backend is running at http://localhost:8000")
        print("[INFO] Frontend will open at: http://localhost:3000")
        print("[INFO] Press Ctrl+C to stop\n")
        
        start_frontend()
        
    else:
        print("[ERROR] Invalid choice. Please run the script again.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n[INFO] SmartWebBot Desktop App stopped")
    except Exception as e:
        print(f"\n[ERROR] An error occurred: {e}")
        print("[INFO] Please check the logs above for more details.")

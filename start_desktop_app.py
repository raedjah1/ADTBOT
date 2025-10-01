"""
SmartWebBot Desktop App Launcher

This script starts both the Python backend and prepares for the Electron frontend.
"""

import os
import sys
import time
import subprocess
import threading
from pathlib import Path

def check_node_installed():
    """Check if Node.js is installed."""
    # First try to find Node.js in common Windows locations
    node_paths = [
        r"C:\Program Files\nodejs",
        r"C:\Program Files (x86)\nodejs",
        os.path.expanduser("~\\AppData\\Roaming\\npm")
    ]
    
    # Add Node.js paths to environment PATH if they exist
    current_path = os.environ.get('PATH', '')
    for node_path in node_paths:
        if os.path.exists(node_path) and node_path not in current_path:
            os.environ['PATH'] = f"{node_path};{current_path}"
            print(f"📍 Added {node_path} to PATH")
    
    try:
        result = subprocess.run(['node', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            version = result.stdout.strip()
            print(f"✅ Node.js found: {version}")
            return True
        else:
            print("❌ Node.js not found")
            return False
    except FileNotFoundError:
        print("❌ Node.js not found")
        print("💡 Checked common installation paths:")
        for path in node_paths:
            exists = "✅" if os.path.exists(path) else "❌"
            print(f"   {exists} {path}")
        return False

def install_frontend_dependencies():
    """Install frontend dependencies."""
    frontend_dir = Path("frontend")
    
    if not frontend_dir.exists():
        print("❌ Frontend directory not found")
        return False
    
    # Check if node_modules already exists
    if (frontend_dir / "node_modules").exists():
        print("✅ Frontend dependencies already installed")
        return True
    
    print("📦 Installing frontend dependencies...")
    
    try:
        # Change to frontend directory and install dependencies
        result = subprocess.run(
            ['npm', 'install', '--legacy-peer-deps'], 
            cwd=frontend_dir,
            capture_output=True,
            text=True,
            env=os.environ  # Use the updated environment with Node.js in PATH
        )
        
        if result.returncode == 0:
            print("✅ Frontend dependencies installed successfully")
            return True
        else:
            print(f"❌ Failed to install dependencies: {result.stderr}")
            return False
            
    except FileNotFoundError:
        print("❌ npm not found. Please install Node.js")
        return False

def start_backend():
    """Start the Python backend server."""
    print("🚀 Starting Python backend server...")
    
    try:
        # Start the backend server
        subprocess.run([sys.executable, 'backend_server.py'])
    except KeyboardInterrupt:
        print("\n🛑 Backend server stopped")
    except Exception as e:
        print(f"❌ Failed to start backend: {e}")

def start_frontend():
    """Start the Electron frontend."""
    print("🖥️ Starting Electron frontend...")
    
    frontend_dir = Path("frontend")
    
    try:
        # Start the frontend in development mode
        subprocess.run(['npm', 'run', 'electron-dev'], cwd=frontend_dir, env=os.environ)
    except KeyboardInterrupt:
        print("\n🛑 Frontend stopped")
    except Exception as e:
        print(f"❌ Failed to start frontend: {e}")

def main():
    """Main launcher function."""
    print("SmartWebBot Desktop App Launcher")
    print("=" * 50)
    
    # Check Node.js
    if not check_node_installed():
        print("\n💡 Please install Node.js from: https://nodejs.org/")
        print("   Then run this script again.")
        return
    
    # Install frontend dependencies
    if not install_frontend_dependencies():
        print("\n❌ Failed to set up frontend dependencies")
        return
    
    print("\n🎉 Setup complete! Choose how to run the app:")
    print("1. Full Desktop App (Electron + Python backend)")
    print("2. Backend Only (for development)")
    print("3. Frontend Only (requires backend running separately)")
    
    choice = input("\nEnter your choice (1-3): ").strip()
    
    if choice == "1":
        print("\n🚀 Starting Full Desktop App...")
        print("📡 Backend will start at: http://localhost:8000")
        print("🖥️ Frontend will open automatically")
        print("⚠️ Press Ctrl+C to stop both services\n")
        
        # Start backend in a separate thread
        backend_thread = threading.Thread(target=start_backend, daemon=True)
        backend_thread.start()
        
        # Give backend time to start
        time.sleep(3)
        
        # Start frontend (this will block)
        start_frontend()
        
    elif choice == "2":
        print("\n🚀 Starting Backend Only...")
        print("📡 API will be available at: http://localhost:8000")
        print("📚 API docs at: http://localhost:8000/docs")
        print("⚠️ Press Ctrl+C to stop\n")
        
        start_backend()
        
    elif choice == "3":
        print("\n🖥️ Starting Frontend Only...")
        print("⚠️ Make sure backend is running at http://localhost:8000")
        print("🌐 Frontend will open at: http://localhost:3000")
        print("⚠️ Press Ctrl+C to stop\n")
        
        start_frontend()
        
    else:
        print("❌ Invalid choice. Please run the script again.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n🛑 SmartWebBot Desktop App stopped")
    except Exception as e:
        print(f"\n❌ An error occurred: {e}")
        print("💡 Please check the logs above for more details.")

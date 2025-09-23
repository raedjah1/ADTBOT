"""
Python Bundling Script for SmartWebBot Installers
Creates a portable Python environment with all dependencies
"""

import os
import sys
import shutil
import subprocess
import urllib.request
import zipfile
import tarfile
from pathlib import Path
import platform

class PythonBundler:
    def __init__(self, target_dir="python-bundle"):
        self.target_dir = Path(target_dir)
        self.platform = platform.system().lower()
        self.arch = platform.machine().lower()
        
        # Python version to bundle
        self.python_version = "3.11.9"
        
        print(f"🐍 Python Bundler for {self.platform} ({self.arch})")
        print(f"📦 Target directory: {self.target_dir}")
        
    def clean_target(self):
        """Remove existing target directory"""
        if self.target_dir.exists():
            print(f"🧹 Cleaning {self.target_dir}")
            shutil.rmtree(self.target_dir)
        
        self.target_dir.mkdir(parents=True, exist_ok=True)
        
    def download_python_windows(self):
        """Download and extract portable Python for Windows"""
        if self.arch in ['amd64', 'x86_64']:
            python_url = f"https://www.python.org/ftp/python/{self.python_version}/python-{self.python_version}-embed-amd64.zip"
            filename = f"python-{self.python_version}-embed-amd64.zip"
        else:
            python_url = f"https://www.python.org/ftp/python/{self.python_version}/python-{self.python_version}-embed-win32.zip"
            filename = f"python-{self.python_version}-embed-win32.zip"
            
        print(f"📥 Downloading Python {self.python_version} for Windows...")
        
        if not Path(filename).exists():
            urllib.request.urlretrieve(python_url, filename)
            print(f"✅ Downloaded {filename}")
        else:
            print(f"✅ Using existing {filename}")
            
        # Extract Python
        print("📦 Extracting Python...")
        with zipfile.ZipFile(filename, 'r') as zip_ref:
            zip_ref.extractall(self.target_dir)
            
        # Download and install pip
        print("📥 Installing pip...")
        get_pip_url = "https://bootstrap.pypa.io/get-pip.py"
        get_pip_path = self.target_dir / "get-pip.py"
        
        urllib.request.urlretrieve(get_pip_url, get_pip_path)
        
        # Run pip installation
        python_exe = self.target_dir / "python.exe"
        subprocess.run([
            str(python_exe), 
            str(get_pip_path), 
            "--target", str(self.target_dir / "Lib" / "site-packages")
        ], check=True)
        
        # Enable site-packages
        pth_file = self.target_dir / f"python{self.python_version.replace('.', '')[:2]}._pth"
        with open(pth_file, 'a') as f:
            f.write("\nimport site\nsite.main()\n")
            
        print("✅ Python for Windows ready")
        
    def download_python_macos(self):
        """Download and extract Python for macOS"""
        python_url = f"https://www.python.org/ftp/python/{self.python_version}/python-{self.python_version}-macos11.pkg"
        filename = f"python-{self.python_version}-macos11.pkg"
        
        print(f"📥 Downloading Python {self.python_version} for macOS...")
        
        if not Path(filename).exists():
            urllib.request.urlretrieve(python_url, filename)
            print(f"✅ Downloaded {filename}")
        else:
            print(f"✅ Using existing {filename}")
            
        # Extract Python framework from pkg
        print("📦 Extracting Python framework...")
        
        # Create temporary extraction directory
        temp_dir = Path("temp_python_extract")
        if temp_dir.exists():
            shutil.rmtree(temp_dir)
        temp_dir.mkdir()
        
        # Extract the pkg file
        subprocess.run([
            "pkgutil", "--expand", filename, str(temp_dir)
        ], check=True)
        
        # Extract the Python framework
        framework_pkg = temp_dir / "Python_Framework.pkg"
        subprocess.run([
            "tar", "-xf", str(framework_pkg / "Payload"), 
            "-C", str(temp_dir)
        ], check=True)
        
        # Copy Python framework
        framework_src = temp_dir / "Library" / "Frameworks" / "Python.framework"
        framework_dst = self.target_dir / "Python.framework"
        
        shutil.copytree(framework_src, framework_dst)
        
        # Clean up
        shutil.rmtree(temp_dir)
        
        print("✅ Python for macOS ready")
        
    def download_python_linux(self):
        """Download and extract Python for Linux"""
        # For Linux, we'll use pyenv or compile from source
        print("🐧 Linux Python bundling not implemented yet")
        print("💡 Consider using pyenv or system Python with virtual environment")
        
    def install_dependencies(self):
        """Install SmartWebBot dependencies"""
        print("📦 Installing SmartWebBot dependencies...")
        
        # Find Python executable
        if self.platform == "windows":
            python_exe = self.target_dir / "python.exe"
            site_packages = self.target_dir / "Lib" / "site-packages"
        elif self.platform == "darwin":  # macOS
            python_exe = self.target_dir / "Python.framework" / "Versions" / "3.11" / "bin" / "python3"
            site_packages = self.target_dir / "Python.framework" / "Versions" / "3.11" / "lib" / "python3.11" / "site-packages"
        else:
            print("❌ Unsupported platform for dependency installation")
            return
            
        # Install requirements
        requirements_file = Path("../../requirements.txt")
        if requirements_file.exists():
            cmd = [
                str(python_exe), "-m", "pip", "install",
                "-r", str(requirements_file),
                "--target", str(site_packages),
                "--no-warn-script-location"
            ]
            
            print(f"🔧 Running: {' '.join(cmd)}")
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                print("✅ Dependencies installed successfully")
            else:
                print(f"❌ Failed to install dependencies:")
                print(result.stderr)
                
        else:
            print("⚠️ requirements.txt not found, skipping dependency installation")
            
    def create_launcher(self):
        """Create platform-specific launcher"""
        if self.platform == "windows":
            self.create_windows_launcher()
        elif self.platform == "darwin":
            self.create_macos_launcher()
        else:
            print("⚠️ Launcher creation not implemented for this platform")
            
    def create_windows_launcher(self):
        """Create Windows batch launcher"""
        launcher_content = '''@echo off
REM SmartWebBot Launcher
cd /d "%~dp0"

REM Set up environment
set PATH=%~dp0;%~dp0Scripts;%PATH%
set PYTHONPATH=%~dp0Lib\\site-packages;%PYTHONPATH%

REM Launch SmartWebBot
echo 🤖 Starting SmartWebBot...
python.exe start_desktop_app.py

pause
'''
        
        launcher_path = self.target_dir / "SmartWebBot.bat"
        with open(launcher_path, 'w') as f:
            f.write(launcher_content)
            
        print("✅ Windows launcher created")
        
    def create_macos_launcher(self):
        """Create macOS shell launcher"""
        launcher_content = '''#!/bin/bash
# SmartWebBot Launcher for macOS

# Get script directory
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Set up environment
export PATH="$DIR/Python.framework/Versions/3.11/bin:$PATH"
export PYTHONPATH="$DIR/Python.framework/Versions/3.11/lib/python3.11/site-packages:$PYTHONPATH"

# Change to bundle directory
cd "$DIR"

# Launch SmartWebBot
echo "🤖 Starting SmartWebBot..."
python3 start_desktop_app.py
'''
        
        launcher_path = self.target_dir / "SmartWebBot.sh"
        with open(launcher_path, 'w') as f:
            f.write(launcher_content)
            
        # Make executable
        os.chmod(launcher_path, 0o755)
        
        print("✅ macOS launcher created")
        
    def bundle(self):
        """Create complete Python bundle"""
        print("🚀 Starting Python bundling process...")
        
        # Clean target directory
        self.clean_target()
        
        # Download Python for the current platform
        if self.platform == "windows":
            self.download_python_windows()
        elif self.platform == "darwin":
            self.download_python_macos()
        elif self.platform == "linux":
            self.download_python_linux()
        else:
            print(f"❌ Unsupported platform: {self.platform}")
            return False
            
        # Install dependencies
        self.install_dependencies()
        
        # Create launcher
        self.create_launcher()
        
        print("🎉 Python bundle created successfully!")
        print(f"📁 Bundle location: {self.target_dir.absolute()}")
        
        return True

def main():
    """Main bundling function"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Bundle Python for SmartWebBot installers")
    parser.add_argument("--target", default="python-bundle", help="Target directory for bundle")
    parser.add_argument("--clean", action="store_true", help="Clean target directory only")
    
    args = parser.parse_args()
    
    bundler = PythonBundler(args.target)
    
    if args.clean:
        bundler.clean_target()
        print("🧹 Target directory cleaned")
        return
        
    success = bundler.bundle()
    
    if success:
        print("\n✅ Bundling completed successfully!")
        print("📦 You can now use this bundle in your installer")
    else:
        print("\n❌ Bundling failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()

"""
VM Security Testing Setup Script

Helps set up and configure VM-based security testing environment for SmartWebBot.
"""

import os
import sys
import subprocess
import requests
from pathlib import Path


def check_docker_installed():
    """Check if Docker is installed."""
    try:
        result = subprocess.run(['docker', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Docker found: {result.stdout.strip()}")
            return True
        else:
            print("❌ Docker not found")
            return False
    except FileNotFoundError:
        print("❌ Docker not installed")
        return False


def setup_dvwa_docker():
    """Set up DVWA using Docker."""
    print("\n🚀 Setting up DVWA (Damn Vulnerable Web Application)...")
    
    try:
        # Pull and run DVWA
        print("📦 Pulling DVWA Docker image...")
        subprocess.run(['docker', 'pull', 'vulnerables/web-dvwa'], check=True)
        
        print("🚀 Starting DVWA container...")
        subprocess.run([
            'docker', 'run', '--rm', '-d', 
            '--name', 'smartwebbot-dvwa',
            '-p', '8080:80', 
            'vulnerables/web-dvwa'
        ], check=True)
        
        print("✅ DVWA is running at: http://localhost:8080")
        print("   Default login: admin / password")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to setup DVWA: {e}")
        return False


def setup_webgoat_docker():
    """Set up WebGoat using Docker."""
    print("\n🚀 Setting up WebGoat...")
    
    try:
        print("📦 Pulling WebGoat Docker image...")
        subprocess.run(['docker', 'pull', 'webgoat/goatandwolf'], check=True)
        
        print("🚀 Starting WebGoat container...")
        subprocess.run([
            'docker', 'run', '--rm', '-d',
            '--name', 'smartwebbot-webgoat', 
            '-p', '8081:8080',
            'webgoat/goatandwolf'
        ], check=True)
        
        print("✅ WebGoat is running at: http://localhost:8081/WebGoat")
        print("   Create your own account when you first visit")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to setup WebGoat: {e}")
        return False


def setup_mutillidae_docker():
    """Set up Mutillidae using Docker."""
    print("\n🚀 Setting up Mutillidae II...")
    
    try:
        print("📦 Pulling Mutillidae Docker image...")
        subprocess.run(['docker', 'pull', 'citizenstig/nowasp'], check=True)
        
        print("🚀 Starting Mutillidae container...")
        subprocess.run([
            'docker', 'run', '--rm', '-d',
            '--name', 'smartwebbot-mutillidae',
            '-p', '8082:80',
            '-p', '3306:3306',
            'citizenstig/nowasp'
        ], check=True)
        
        print("✅ Mutillidae is running at: http://localhost:8082/mutillidae")
        print("   No login required for most features")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to setup Mutillidae: {e}")
        return False


def check_containers_running():
    """Check which containers are running."""
    print("\n📊 Checking running containers...")
    
    containers = [
        ('smartwebbot-dvwa', 'http://localhost:8080', 'DVWA'),
        ('smartwebbot-webgoat', 'http://localhost:8081/WebGoat', 'WebGoat'),
        ('smartwebbot-mutillidae', 'http://localhost:8082/mutillidae', 'Mutillidae')
    ]
    
    running_containers = []
    
    for container_name, url, app_name in containers:
        try:
            result = subprocess.run(
                ['docker', 'ps', '--filter', f'name={container_name}', '--format', '{{.Names}}'],
                capture_output=True, text=True, check=True
            )
            
            if container_name in result.stdout:
                print(f"✅ {app_name}: Running at {url}")
                running_containers.append((app_name, url))
            else:
                print(f"❌ {app_name}: Not running")
                
        except subprocess.CalledProcessError:
            print(f"❌ {app_name}: Error checking status")
    
    return running_containers


def test_container_accessibility():
    """Test if containers are accessible."""
    print("\n🔍 Testing container accessibility...")
    
    test_urls = [
        ('http://localhost:8080', 'DVWA'),
        ('http://localhost:8081/WebGoat', 'WebGoat'),
        ('http://localhost:8082/mutillidae', 'Mutillidae')
    ]
    
    accessible_apps = []
    
    for url, app_name in test_urls:
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                print(f"✅ {app_name}: Accessible at {url}")
                accessible_apps.append((app_name, url))
            else:
                print(f"⚠️ {app_name}: HTTP {response.status_code} at {url}")
        except requests.RequestException:
            print(f"❌ {app_name}: Not accessible at {url}")
    
    return accessible_apps


def generate_smartwebbot_config(accessible_apps):
    """Generate SmartWebBot configuration for VM testing."""
    print("\n📝 Generating SmartWebBot VM testing configuration...")
    
    config_content = f"""# SmartWebBot VM Testing Configuration
# Generated automatically for your vulnerable applications

# Accessible Applications:
"""
    
    for app_name, url in accessible_apps:
        config_content += f"# - {app_name}: {url}\n"
    
    config_content += """
# Testing Targets (copy these into your SmartWebBot security session):
TARGET_URLS = [
"""
    
    for app_name, url in accessible_apps:
        config_content += f'    "{url}",  # {app_name}\n'
    
    config_content += """]

# Example SmartWebBot Security Testing Session:
# 1. Open SmartWebBot Security Testing module
# 2. Enter password: RaedJah
# 3. Use any of the URLs above as target
# 4. Run comprehensive security tests

# Common Test Scenarios:
# - SQL Injection on DVWA login forms
# - XSS testing on WebGoat lessons
# - Command injection on Mutillidae tools
# - Authentication bypass on all applications
"""
    
    config_file = Path("vm_testing_config.txt")
    config_file.write_text(config_content)
    
    print(f"✅ Configuration saved to: {config_file.absolute()}")
    print("\n📋 Quick Start Guide:")
    print("1. Launch SmartWebBot: python backend_server.py")
    print("2. Open frontend and go to Security Testing")
    print("3. Enter password: RaedJah")
    print("4. Use the URLs above as testing targets")


def cleanup_containers():
    """Clean up all testing containers."""
    print("\n🧹 Cleaning up containers...")
    
    containers = ['smartwebbot-dvwa', 'smartwebbot-webgoat', 'smartwebbot-mutillidae']
    
    for container in containers:
        try:
            subprocess.run(['docker', 'stop', container], 
                         capture_output=True, check=True)
            print(f"✅ Stopped {container}")
        except subprocess.CalledProcessError:
            print(f"⚠️ {container} was not running")


def main():
    """Main setup function."""
    print("🛡️ SmartWebBot VM Security Testing Setup")
    print("=" * 50)
    print("Setting up vulnerable applications for ethical hacking practice")
    print("⚠️ These applications are intentionally vulnerable - use responsibly!")
    print("=" * 50)
    
    # Check Docker
    if not check_docker_installed():
        print("\n💡 Please install Docker Desktop first:")
        print("   Windows/Mac: https://www.docker.com/products/docker-desktop")
        print("   Linux: https://docs.docker.com/engine/install/")
        return
    
    print("\nChoose setup option:")
    print("1. Setup all vulnerable applications (Recommended)")
    print("2. Setup DVWA only (Beginner friendly)")
    print("3. Setup WebGoat only (OWASP focused)")
    print("4. Setup Mutillidae only (Advanced)")
    print("5. Check current status")
    print("6. Cleanup all containers")
    
    choice = input("\nEnter your choice (1-6): ").strip()
    
    if choice == "1":
        setup_dvwa_docker()
        setup_webgoat_docker()
        setup_mutillidae_docker()
    elif choice == "2":
        setup_dvwa_docker()
    elif choice == "3":
        setup_webgoat_docker()
    elif choice == "4":
        setup_mutillidae_docker()
    elif choice == "5":
        running = check_containers_running()
        if running:
            accessible = test_container_accessibility()
            generate_smartwebbot_config(accessible)
        return
    elif choice == "6":
        cleanup_containers()
        return
    else:
        print("❌ Invalid choice")
        return
    
    # Wait for containers to start
    print("\n⏳ Waiting for containers to start...")
    import time
    time.sleep(10)
    
    # Check status and generate config
    running = check_containers_running()
    if running:
        accessible = test_container_accessibility()
        generate_smartwebbot_config(accessible)
        
        print("\n🎉 Setup complete! Your VM testing environment is ready.")
        print("\n🚀 Next steps:")
        print("1. Launch SmartWebBot backend: python backend_server.py")
        print("2. Open the frontend Security Testing module")
        print("3. Enter password: RaedJah")
        print("4. Start testing with the URLs shown above")
        print("\n⚠️ Remember: These are vulnerable applications for learning!")
    else:
        print("\n⚠️ Some containers may still be starting. Wait a few minutes and run option 5 to check status.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n🛑 Setup interrupted by user")
    except Exception as e:
        print(f"\n❌ An error occurred: {e}")
        print("💡 Please check Docker is running and try again")

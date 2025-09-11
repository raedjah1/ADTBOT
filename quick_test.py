"""
Quick verification script for SmartWebBot v2.0

Fast test to verify the bot is ready to use.
"""

def main():
    print("🚀 SmartWebBot v2.0 - Quick Setup Check")
    print("=" * 45)
    
    # Test 1: Core imports
    print("📦 Testing core imports...", end=" ")
    try:
        from smartwebbot import SmartWebBot, smart_bot
        print("✅")
    except Exception as e:
        print(f"❌ {e}")
        return False
    
    # Test 2: Essential dependencies
    print("📋 Testing key dependencies...", end=" ")
    try:
        import selenium
        import yaml
        import requests
        print("✅")
    except Exception as e:
        print(f"❌ {e}")
        return False
    
    # Test 3: Configuration
    print("⚙️ Testing configuration...", end=" ")
    try:
        from smartwebbot.utils.config_manager import get_config_manager
        config = get_config_manager()
        browser = config.get('browser.default_browser', 'chrome')
        print("✅")
    except Exception as e:
        print(f"❌ {e}")
        return False
    
    # Test 4: CLI
    print("🖥️ Testing CLI interface...", end=" ")
    try:
        import cli
        print("✅")
    except Exception as e:
        print(f"❌ {e}")
        return False
    
    print("\n🎉 SmartWebBot is ready to use!")
    print("\n🚀 Try these commands:")
    print("   python cli.py version")
    print("   python cli.py --help")
    print("   python example_usage.py")
    
    print("\n💡 Tips:")
    print("   • Make sure Chrome/Firefox is installed for browser automation")
    print("   • Edit config.yaml to customize settings")
    print("   • Check README.md for detailed usage examples")
    
    return True

if __name__ == "__main__":
    success = main()
    if not success:
        print("\n⚠️ Setup issues detected. Try:")
        print("   pip install -r requirements.txt")
    exit(0 if success else 1)

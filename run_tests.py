"""
Test runner for SmartWebBot

Runs all tests and provides comprehensive reporting.
"""

import sys
import subprocess
import os
from pathlib import Path


def install_test_dependencies():
    """Install required test dependencies."""
    print("📦 Installing test dependencies...")
    
    test_deps = [
        "pytest>=7.4.0",
        "pytest-asyncio>=0.21.0",
        "pytest-mock>=3.11.0", 
        "httpx>=0.24.0",  # For FastAPI test client
        "ollama>=0.1.0",  # For AI chat testing
    ]
    
    for dep in test_deps:
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", dep], 
                          check=True, capture_output=True)
            print(f"✅ Installed {dep}")
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to install {dep}: {e}")
            return False
    
    return True


def run_tests():
    """Run all tests with detailed reporting."""
    print("\n🧪 Running SmartWebBot Tests")
    print("=" * 50)
    
    # Test categories
    test_categories = [
        ("AI Chat Tests", "tests/test_chat_ai.py"),
        ("Core Bot Tests", "tests/test_smartwebbot_core.py"), 
        ("Backend API Tests", "tests/test_backend_api.py")
    ]
    
    results = {}
    
    for category, test_file in test_categories:
        print(f"\n🔍 Running {category}...")
        
        if not Path(test_file).exists():
            print(f"❌ Test file not found: {test_file}")
            results[category] = {"status": "missing", "details": "Test file not found"}
            continue
        
        try:
            # Run pytest with verbose output
            result = subprocess.run([
                sys.executable, "-m", "pytest", 
                test_file, 
                "-v",  # Verbose
                "--tb=short",  # Short traceback format
                "--no-header",  # No header
                "-q"  # Quiet
            ], capture_output=True, text=True, timeout=60)
            
            if result.returncode == 0:
                print(f"✅ {category} - All tests passed")
                results[category] = {"status": "passed", "output": result.stdout}
            else:
                print(f"❌ {category} - Some tests failed")
                results[category] = {"status": "failed", "output": result.stdout, "errors": result.stderr}
                
        except subprocess.TimeoutExpired:
            print(f"⏰ {category} - Tests timed out")
            results[category] = {"status": "timeout", "details": "Tests exceeded 60 second timeout"}
        except Exception as e:
            print(f"💥 {category} - Error running tests: {e}")
            results[category] = {"status": "error", "details": str(e)}
    
    return results


def run_manual_tests():
    """Run manual verification tests."""
    print("\n🔧 Manual Verification Tests")
    print("=" * 30)
    
    tests = []
    
    # Test 1: Check if SmartWebBot can be imported
    print("1. Testing SmartWebBot import...")
    try:
        from smartwebbot import SmartWebBot
        print("   ✅ SmartWebBot imports successfully")
        tests.append(("Import SmartWebBot", True))
    except Exception as e:
        print(f"   ❌ SmartWebBot import failed: {e}")
        tests.append(("Import SmartWebBot", False))
    
    # Test 2: Check AI Chat import
    print("2. Testing AI Chat import...")
    try:
        from smartwebbot.intelligence.chat_ai import ChatAI
        print("   ✅ ChatAI imports successfully")
        tests.append(("Import ChatAI", True))
    except Exception as e:
        print(f"   ❌ ChatAI import failed: {e}")
        tests.append(("Import ChatAI", False))
    
    # Test 3: Check Form Handler
    print("3. Testing Form Handler import...")
    try:
        from smartwebbot.automation.form_handler import FormHandler
        print("   ✅ FormHandler imports successfully")
        tests.append(("Import FormHandler", True))
    except Exception as e:
        print(f"   ❌ FormHandler import failed: {e}")
        tests.append(("Import FormHandler", False))
    
    # Test 4: Check Backend Server
    print("4. Testing Backend Server import...")
    try:
        import backend_server
        print("   ✅ Backend server imports successfully")
        tests.append(("Import Backend", True))
    except Exception as e:
        print(f"   ❌ Backend server import failed: {e}")
        tests.append(("Import Backend", False))
    
    # Test 5: Check if Ollama is available (optional)
    print("5. Testing Ollama availability...")
    try:
        import ollama
        ollama.list()  # Test connection
        print("   ✅ Ollama is available and running")
        tests.append(("Ollama Available", True))
    except ImportError:
        print("   ⚠️ Ollama not installed (optional for AI chat)")
        tests.append(("Ollama Available", False))
    except Exception as e:
        print(f"   ⚠️ Ollama not running: {e}")
        tests.append(("Ollama Available", False))
    
    return tests


def test_basic_functionality():
    """Test basic SmartWebBot functionality without browser."""
    print("\n⚙️ Basic Functionality Tests")
    print("=" * 30)
    
    tests = []
    
    # Test SmartWebBot initialization
    print("1. Testing SmartWebBot initialization...")
    try:
        from smartwebbot import SmartWebBot
        
        config = {
            "browser": {"default_browser": "chrome", "headless": True},
            "automation": {"wait_time": 1}
        }
        
        bot = SmartWebBot(config_dict=config)
        print("   ✅ SmartWebBot created successfully")
        tests.append(("Bot Creation", True))
        
        # Test configuration
        if hasattr(bot, 'config'):
            print("   ✅ Bot has configuration")
            tests.append(("Bot Config", True))
        else:
            print("   ❌ Bot missing configuration")
            tests.append(("Bot Config", False))
            
    except Exception as e:
        print(f"   ❌ SmartWebBot initialization failed: {e}")
        tests.append(("Bot Creation", False))
        tests.append(("Bot Config", False))
    
    # Test AI Chat initialization
    print("2. Testing AI Chat initialization...")
    try:
        from smartwebbot.intelligence.chat_ai import ChatAI
        
        chat_ai = ChatAI({"provider": "ollama", "model": "llama3.2:3b"})
        print("   ✅ ChatAI created successfully")
        tests.append(("ChatAI Creation", True))
        
        # Test system prompt
        prompt = chat_ai._create_system_prompt()
        if "SmartWebBot" in prompt:
            print("   ✅ System prompt generated correctly")
            tests.append(("System Prompt", True))
        else:
            print("   ❌ System prompt missing key content")
            tests.append(("System Prompt", False))
            
    except Exception as e:
        print(f"   ❌ ChatAI initialization failed: {e}")
        tests.append(("ChatAI Creation", False))
        tests.append(("System Prompt", False))
    
    return tests


def generate_test_report(pytest_results, manual_results, functionality_results):
    """Generate comprehensive test report."""
    print("\n📊 Test Report Summary")
    print("=" * 50)
    
    total_tests = 0
    passed_tests = 0
    
    # Pytest results
    print("\n🧪 Automated Test Results:")
    for category, result in pytest_results.items():
        status_icon = "✅" if result["status"] == "passed" else "❌"
        print(f"  {status_icon} {category}: {result['status']}")
        total_tests += 1
        if result["status"] == "passed":
            passed_tests += 1
    
    # Manual test results
    print("\n🔧 Manual Test Results:")
    for test_name, passed in manual_results:
        status_icon = "✅" if passed else "❌"
        print(f"  {status_icon} {test_name}")
        total_tests += 1
        if passed:
            passed_tests += 1
    
    # Functionality test results
    print("\n⚙️ Functionality Test Results:")
    for test_name, passed in functionality_results:
        status_icon = "✅" if passed else "❌"
        print(f"  {status_icon} {test_name}")
        total_tests += 1
        if passed:
            passed_tests += 1
    
    # Overall summary
    print(f"\n📈 Overall Results:")
    print(f"  Total Tests: {total_tests}")
    print(f"  Passed: {passed_tests}")
    print(f"  Failed: {total_tests - passed_tests}")
    print(f"  Success Rate: {(passed_tests/total_tests)*100:.1f}%")
    
    # Recommendations
    print(f"\n💡 Recommendations:")
    if passed_tests == total_tests:
        print("  🎉 All tests passed! SmartWebBot is ready to use.")
    elif passed_tests >= total_tests * 0.8:
        print("  👍 Most tests passed. Minor issues may exist but core functionality works.")
    else:
        print("  ⚠️ Several tests failed. Please review errors before using SmartWebBot.")
    
    # Next steps
    print(f"\n🚀 Next Steps:")
    print("  1. Review any failed tests above")
    print("  2. Install missing dependencies if needed")
    print("  3. For AI chat: Install Ollama and pull a model (ollama pull llama3.2:3b)")
    print("  4. Test with real websites using the desktop app")


def main():
    """Main test runner."""
    print("🤖 SmartWebBot Test Suite")
    print("=" * 40)
    
    # Install dependencies
    if not install_test_dependencies():
        print("❌ Failed to install test dependencies")
        return 1
    
    # Run different test categories
    pytest_results = run_tests()
    manual_results = run_manual_tests() 
    functionality_results = test_basic_functionality()
    
    # Generate report
    generate_test_report(pytest_results, manual_results, functionality_results)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())

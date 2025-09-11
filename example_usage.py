"""
SmartWebBot v2.0 - Example Usage

This script demonstrates the advanced capabilities of the intelligent web automation system.
"""

import time
import asyncio
from smartwebbot import SmartWebBot, smart_bot


def basic_automation_example():
    """Demonstrate basic automation capabilities."""
    print("🤖 SmartWebBot v2.0 - Basic Automation Example")
    print("=" * 50)
    
    with smart_bot() as bot:
        # Navigate to a test page
        print("📍 Navigating to test page...")
        bot.navigate_to("https://httpbin.org/forms/post")
        
        # Fill a form intelligently
        print("📝 Filling form with AI-powered field detection...")
        form_data = {
            "customer name": "John Doe",
            "customer telephone": "123-456-7890", 
            "customer email": "john@example.com",
            "pizza size": "large"
        }
        
        success = bot.fill_form_intelligently(form_data)
        print(f"✅ Form filled: {'Success' if success else 'Failed'}")
        
        # Take a screenshot
        print("📸 Taking screenshot...")
        screenshot_path = bot.take_screenshot("form_filled_example.png")
        print(f"📁 Screenshot saved: {screenshot_path}")
        
        # Demonstrate intelligent clicking
        print("🖱️ Clicking submit button intelligently...")
        click_success = bot.click_element("submit button", intelligent=True)
        print(f"✅ Button clicked: {'Success' if click_success else 'Failed'}")


def advanced_intelligence_example():
    """Demonstrate advanced AI capabilities."""
    print("\n🧠 SmartWebBot v2.0 - Advanced Intelligence Example")
    print("=" * 50)
    
    with smart_bot() as bot:
        # Navigate to a complex page
        print("📍 Navigating to complex page...")
        bot.navigate_to("https://www.example.com")
        
        # Perform intelligent task
        print("🎯 Performing intelligent task...")
        result = bot.perform_task("find the main heading and click it")
        print(f"📊 Task result: {result}")
        
        # Intelligent waiting
        print("⏳ Waiting intelligently for page changes...")
        wait_success = bot.wait_intelligently("page has loaded completely", timeout=10)
        print(f"✅ Wait completed: {'Success' if wait_success else 'Timeout'}")
        
        # Extract data intelligently
        print("📊 Extracting data with AI...")
        data = bot.extract_data_intelligently("all links on the page")
        print(f"📈 Extracted {len(data)} data items")


def performance_monitoring_example():
    """Demonstrate performance monitoring capabilities."""
    print("\n📊 SmartWebBot v2.0 - Performance Monitoring Example")
    print("=" * 50)
    
    with smart_bot() as bot:
        # Perform several operations
        operations = [
            ("https://httpbin.org/html", "Navigate to HTML page"),
            ("https://httpbin.org/json", "Navigate to JSON page"),
            ("https://httpbin.org/xml", "Navigate to XML page")
        ]
        
        for url, description in operations:
            print(f"🔄 {description}...")
            start_time = time.time()
            bot.navigate_to(url)
            duration = time.time() - start_time
            print(f"⏱️ Completed in {duration:.2f}s")
        
        # Get comprehensive performance report
        print("\n📈 Generating performance report...")
        report = bot.get_performance_report()
        
        print(f"📊 Performance Summary:")
        print(f"   • Total Tasks: {report.get('task_summary', {}).get('total_tasks', 0)}")
        print(f"   • Success Rate: {report.get('task_summary', {}).get('successful_tasks', 0)}")
        print(f"   • Avg Duration: {report.get('task_summary', {}).get('average_task_duration', 0):.2f}s")


def plugin_system_example():
    """Demonstrate the plugin system."""
    print("\n🔌 SmartWebBot v2.0 - Plugin System Example")
    print("=" * 50)
    
    # Example custom plugin
    class CustomAnalyzerPlugin:
        def __init__(self, config):
            self.config = config
        
        def initialize(self):
            return True
        
        def analyze_page(self, url):
            return {
                'url': url,
                'analysis': 'Custom analysis performed',
                'timestamp': time.time()
            }
    
    with smart_bot() as bot:
        # Register the plugin
        print("🔧 Registering custom plugin...")
        plugin_success = bot.register_plugin("custom_analyzer", CustomAnalyzerPlugin, {})
        print(f"✅ Plugin registered: {'Success' if plugin_success else 'Failed'}")
        
        if plugin_success:
            # Use the plugin
            print("🎯 Executing plugin method...")
            result = bot.execute_plugin("custom_analyzer", "analyze_page", "https://example.com")
            print(f"📊 Plugin result: {result}")


def error_handling_example():
    """Demonstrate error handling and recovery."""
    print("\n🛡️ SmartWebBot v2.0 - Error Handling Example")
    print("=" * 50)
    
    with smart_bot() as bot:
        # Try to navigate to invalid URL
        print("🚫 Testing error handling with invalid URL...")
        success = bot.navigate_to("https://this-domain-does-not-exist.invalid")
        print(f"📊 Navigation result: {'Success' if success else 'Failed (as expected)'}")
        
        # Try to find non-existent element
        print("🔍 Testing AI detection with non-existent element...")
        element = bot.find_element_intelligently("non-existent magical button")
        print(f"📊 Element found: {'Yes' if element else 'No (as expected)'}")
        
        # Demonstrate retry logic
        print("🔄 Testing retry logic...")
        task_result = bot.perform_task("click the invisible button that doesn't exist")
        print(f"📊 Task completed: {task_result.get('success', False)}")


def real_world_automation_example():
    """Demonstrate real-world automation scenario."""
    print("\n🌍 SmartWebBot v2.0 - Real-World Automation Example")
    print("=" * 50)
    
    with smart_bot() as bot:
        # Simulate a real automation task
        print("🎯 Simulating real-world automation task...")
        
        # Navigate to a form page
        bot.navigate_to("https://httpbin.org/forms/post")
        
        # Fill out a contact form
        contact_data = {
            "name": "SmartWebBot User",
            "email": "user@smartwebbot.com",
            "message": "This is an automated message from SmartWebBot v2.0!"
        }
        
        print("📝 Filling contact form...")
        form_success = bot.fill_form_intelligently(contact_data)
        
        # Take screenshot for verification
        screenshot = bot.take_screenshot("contact_form_filled.png")
        
        # Submit the form
        print("📤 Submitting form...")
        submit_success = bot.perform_task("submit the form")
        
        print(f"✅ Automation completed:")
        print(f"   • Form filled: {'Success' if form_success else 'Failed'}")
        print(f"   • Screenshot: {screenshot}")
        print(f"   • Form submitted: {submit_success.get('success', False)}")


def main():
    """Main example runner."""
    print("🚀 SmartWebBot v2.0 - Comprehensive Example Suite")
    print("=" * 60)
    print("Demonstrating state-of-the-art intelligent web automation")
    print("=" * 60)
    
    examples = [
        ("Basic Automation", basic_automation_example),
        ("Advanced Intelligence", advanced_intelligence_example),
        ("Performance Monitoring", performance_monitoring_example),
        ("Plugin System", plugin_system_example),
        ("Error Handling", error_handling_example),
        ("Real-World Automation", real_world_automation_example)
    ]
    
    for name, example_func in examples:
        try:
            print(f"\n🎬 Running {name} Example...")
            example_func()
            print(f"✅ {name} Example completed successfully!")
        except Exception as e:
            print(f"❌ {name} Example failed: {e}")
        
        print("\n" + "-" * 50)
        time.sleep(1)  # Brief pause between examples
    
    print("\n🎉 All examples completed!")
    print("🔗 For more information, visit: https://github.com/smartwebbot/smartwebbot")


if __name__ == "__main__":
    main()

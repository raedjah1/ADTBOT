"""
SmartWebBot v2.0 - Command Line Interface

Advanced CLI for intelligent web automation.
"""

import click
import json
import sys
from pathlib import Path
from typing import Dict, Any

from smartwebbot import SmartWebBot, smart_bot
from smartwebbot.utils.config_manager import get_config_manager


@click.group()
@click.version_option(version='2.0.0', prog_name='SmartWebBot')
@click.option('--config', '-c', type=click.Path(exists=True), 
              help='Path to configuration file')
@click.option('--verbose', '-v', is_flag=True, help='Enable verbose logging')
@click.pass_context
def cli(ctx, config, verbose):
    """SmartWebBot v2.0 - Intelligent Web Automation CLI"""
    ctx.ensure_object(dict)
    ctx.obj['config'] = config
    ctx.obj['verbose'] = verbose
    
    if verbose:
        click.echo("🤖 SmartWebBot v2.0 - Intelligent Web Automation")
        click.echo("=" * 50)


@cli.command()
@click.option('--url', '-u', required=True, help='URL to navigate to')
@click.option('--screenshot', '-s', is_flag=True, help='Take screenshot after navigation')
@click.option('--wait', '-w', type=int, default=3, help='Wait time after navigation')
@click.pass_context
def navigate(ctx, url, screenshot, wait):
    """Navigate to a URL with intelligent loading detection."""
    click.echo(f"🌐 Navigating to: {url}")
    
    try:
        with smart_bot(config_path=ctx.obj.get('config')) as bot:
            success = bot.navigate_to(url)
            
            if success:
                click.echo("✅ Navigation successful")
                
                if wait:
                    import time
                    time.sleep(wait)
                
                if screenshot:
                    screenshot_path = bot.take_screenshot()
                    click.echo(f"📸 Screenshot saved: {screenshot_path}")
            else:
                click.echo("❌ Navigation failed")
                sys.exit(1)
                
    except Exception as e:
        click.echo(f"❌ Error: {e}")
        sys.exit(1)


@cli.command()
@click.option('--url', '-u', required=True, help='URL to navigate to')
@click.option('--data', '-d', required=True, help='Form data as JSON string')
@click.option('--submit', '-s', is_flag=True, help='Submit form after filling')
@click.pass_context
def fill_form(ctx, url, data, submit):
    """Fill a form using intelligent field detection."""
    click.echo(f"📝 Filling form at: {url}")
    
    try:
        # Parse form data
        try:
            form_data = json.loads(data)
        except json.JSONDecodeError:
            click.echo("❌ Invalid JSON in --data parameter")
            sys.exit(1)
        
        with smart_bot(config_path=ctx.obj.get('config')) as bot:
            # Navigate to URL
            if not bot.navigate_to(url):
                click.echo("❌ Navigation failed")
                sys.exit(1)
            
            # Fill form
            success = bot.fill_form_intelligently(form_data)
            
            if success:
                click.echo("✅ Form filled successfully")
                
                if submit:
                    submit_result = bot.perform_task("submit the form")
                    if submit_result.get('success'):
                        click.echo("✅ Form submitted successfully")
                    else:
                        click.echo("❌ Form submission failed")
            else:
                click.echo("❌ Form filling failed")
                sys.exit(1)
                
    except Exception as e:
        click.echo(f"❌ Error: {e}")
        sys.exit(1)


@cli.command()
@click.option('--url', '-u', required=True, help='URL to extract data from')
@click.option('--description', '-d', required=True, help='Description of data to extract')
@click.option('--output', '-o', help='Output file path')
@click.option('--format', '-f', type=click.Choice(['csv', 'json']), default='csv', 
              help='Output format')
@click.pass_context
def extract_data(ctx, url, description, output, format):
    """Extract data from a webpage using AI."""
    click.echo(f"📊 Extracting data from: {url}")
    click.echo(f"🎯 Looking for: {description}")
    
    try:
        with smart_bot(config_path=ctx.obj.get('config')) as bot:
            # Navigate to URL
            if not bot.navigate_to(url):
                click.echo("❌ Navigation failed")
                sys.exit(1)
            
            # Extract data
            data = bot.extract_data_intelligently(description)
            
            if data:
                click.echo(f"✅ Extracted {len(data)} items")
                
                # Export data if output specified
                if output:
                    from smartwebbot.data.exporter import DataExporter
                    exporter = DataExporter()
                    exporter.initialize()
                    
                    if exporter.export_data(data, output, format):
                        click.echo(f"💾 Data exported to: {output}")
                    else:
                        click.echo("❌ Export failed")
                else:
                    # Print first few items
                    for i, item in enumerate(data[:3]):
                        click.echo(f"📄 Item {i+1}: {item}")
                    if len(data) > 3:
                        click.echo(f"... and {len(data) - 3} more items")
            else:
                click.echo("❌ No data extracted")
                
    except Exception as e:
        click.echo(f"❌ Error: {e}")
        sys.exit(1)


@cli.command()
@click.option('--url', '-u', required=True, help='URL to perform task on')
@click.option('--task', '-t', required=True, help='Task description')
@click.option('--screenshot', '-s', is_flag=True, help='Take screenshot after task')
@click.pass_context
def perform_task(ctx, url, task, screenshot):
    """Perform an intelligent automation task."""
    click.echo(f"🎯 Performing task: {task}")
    click.echo(f"🌐 On URL: {url}")
    
    try:
        with smart_bot(config_path=ctx.obj.get('config')) as bot:
            # Navigate to URL
            if not bot.navigate_to(url):
                click.echo("❌ Navigation failed")
                sys.exit(1)
            
            # Perform task
            result = bot.perform_task(task)
            
            if result.get('success'):
                click.echo("✅ Task completed successfully")
                click.echo(f"🤖 Action: {result.get('action_type', 'unknown')}")
                click.echo(f"🎯 Confidence: {result.get('confidence', 0):.2f}")
                click.echo(f"💭 Reasoning: {result.get('reasoning', 'N/A')}")
                
                if screenshot:
                    screenshot_path = bot.take_screenshot()
                    click.echo(f"📸 Screenshot saved: {screenshot_path}")
            else:
                click.echo("❌ Task failed")
                if result.get('error'):
                    click.echo(f"🚫 Error: {result['error']}")
                sys.exit(1)
                
    except Exception as e:
        click.echo(f"❌ Error: {e}")
        sys.exit(1)


@cli.command()
@click.option('--output', '-o', help='Output file for report')
@click.pass_context
def performance_report(ctx, output):
    """Generate a comprehensive performance report."""
    click.echo("📊 Generating performance report...")
    
    try:
        with smart_bot(config_path=ctx.obj.get('config')) as bot:
            # Perform some test operations
            test_urls = [
                "https://httpbin.org/html",
                "https://httpbin.org/json",
                "https://httpbin.org/xml"
            ]
            
            click.echo("🔄 Running performance tests...")
            for url in test_urls:
                bot.navigate_to(url)
                click.echo(f"✅ Tested: {url}")
            
            # Generate report
            report = bot.get_performance_report()
            
            if output:
                with open(output, 'w') as f:
                    json.dump(report, f, indent=2, default=str)
                click.echo(f"💾 Report saved to: {output}")
            else:
                click.echo("\n📈 Performance Summary:")
                task_summary = report.get('task_summary', {})
                click.echo(f"   • Total Tasks: {task_summary.get('total_tasks', 0)}")
                click.echo(f"   • Successful Tasks: {task_summary.get('successful_tasks', 0)}")
                click.echo(f"   • Average Duration: {task_summary.get('average_task_duration', 0):.2f}s")
                
                browser_perf = report.get('browser_performance', {})
                if browser_perf:
                    click.echo(f"   • Page Load Time: {browser_perf.get('averagePageLoadTime', 0):.2f}s")
                    click.echo(f"   • Total Page Loads: {browser_perf.get('totalPageLoads', 0)}")
                
    except Exception as e:
        click.echo(f"❌ Error: {e}")
        sys.exit(1)


@cli.command()
@click.pass_context
def config_info(ctx):
    """Display current configuration information."""
    click.echo("⚙️ SmartWebBot Configuration")
    click.echo("=" * 30)
    
    try:
        config_manager = get_config_manager()
        if ctx.obj.get('config'):
            config_manager.config_path = Path(ctx.obj['config'])
            config_manager.load_configuration()
        
        summary = config_manager.get_config_summary()
        
        click.echo(f"📁 Config File: {summary['config_file']}")
        click.echo(f"📄 File Exists: {summary['file_exists']}")
        
        click.echo("\n🌐 Browser Settings:")
        browser = summary['browser']
        click.echo(f"   • Default Browser: {browser['default_browser']}")
        click.echo(f"   • Headless Mode: {browser['headless']}")
        click.echo(f"   • Window Size: {browser['window_size']}")
        
        click.echo("\n🤖 Automation Settings:")
        automation = summary['automation']
        click.echo(f"   • Screenshot on Error: {automation['screenshot_on_error']}")
        click.echo(f"   • Retry Attempts: {automation['retry_attempts']}")
        click.echo(f"   • Human-like Delays: {automation['human_like_delays']}")
        
        click.echo("\n🧠 AI Settings:")
        ai = summary['ai']
        click.echo(f"   • AI Enabled: {ai['enabled']}")
        click.echo(f"   • Confidence Threshold: {ai['confidence_threshold']}")
        click.echo(f"   • Learning Enabled: {ai['learning_enabled']}")
        
    except Exception as e:
        click.echo(f"❌ Error: {e}")
        sys.exit(1)


@cli.command()
@click.pass_context
def version(ctx):
    """Display version and system information."""
    click.echo("🤖 SmartWebBot v2.0 - System Information")
    click.echo("=" * 40)
    
    try:
        import platform
        import sys
        from selenium import __version__ as selenium_version
        
        click.echo(f"🐍 Python Version: {sys.version}")
        click.echo(f"💻 Platform: {platform.platform()}")
        click.echo(f"🌐 Selenium Version: {selenium_version}")
        click.echo(f"🤖 SmartWebBot Version: 2.0.0")
        
        click.echo("\n🎯 Features:")
        click.echo("   ✅ AI-Powered Element Detection")
        click.echo("   ✅ Intelligent Decision Making")
        click.echo("   ✅ Multi-Browser Support")
        click.echo("   ✅ Advanced Error Handling")
        click.echo("   ✅ Performance Monitoring")
        click.echo("   ✅ Plugin System")
        click.echo("   ✅ Security Features")
        
    except Exception as e:
        click.echo(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    cli()

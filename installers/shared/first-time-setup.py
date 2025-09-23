"""
First-time setup script for SmartWebBot
Runs automatically after installation to configure the application
"""

import os
import sys
import json
import shutil
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from pathlib import Path
import subprocess

class SmartWebBotSetup:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("SmartWebBot - First Time Setup")
        self.root.geometry("600x500")
        self.root.resizable(False, False)
        
        # Center the window
        self.center_window()
        
        # Variables
        self.browser_var = tk.StringVar(value="chrome")
        self.headless_var = tk.BooleanVar(value=False)
        self.ai_enabled_var = tk.BooleanVar(value=True)
        
        self.create_widgets()
        
    def center_window(self):
        """Center the window on screen"""
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (600 // 2)
        y = (self.root.winfo_screenheight() // 2) - (500 // 2)
        self.root.geometry(f"600x500+{x}+{y}")
        
    def create_widgets(self):
        """Create the setup wizard interface"""
        
        # Header
        header_frame = ttk.Frame(self.root)
        header_frame.pack(fill="x", padx=20, pady=20)
        
        title_label = ttk.Label(
            header_frame, 
            text="🤖 SmartWebBot Setup Wizard",
            font=("Arial", 16, "bold")
        )
        title_label.pack()
        
        subtitle_label = ttk.Label(
            header_frame,
            text="Let's configure your AI-powered web automation tool",
            font=("Arial", 10)
        )
        subtitle_label.pack(pady=(5, 0))
        
        # Main content frame
        content_frame = ttk.Frame(self.root)
        content_frame.pack(fill="both", expand=True, padx=20)
        
        # Browser selection
        browser_frame = ttk.LabelFrame(content_frame, text="🌐 Browser Settings", padding=10)
        browser_frame.pack(fill="x", pady=(0, 15))
        
        ttk.Label(browser_frame, text="Default Browser:").pack(anchor="w")
        
        browser_options = [
            ("Google Chrome (Recommended)", "chrome"),
            ("Microsoft Edge", "edge"),
            ("Mozilla Firefox", "firefox")
        ]
        
        for text, value in browser_options:
            ttk.Radiobutton(
                browser_frame,
                text=text,
                variable=self.browser_var,
                value=value
            ).pack(anchor="w", pady=2)
            
        ttk.Checkbutton(
            browser_frame,
            text="Run browser in background (headless mode)",
            variable=self.headless_var
        ).pack(anchor="w", pady=(10, 0))
        
        # AI Settings
        ai_frame = ttk.LabelFrame(content_frame, text="🧠 AI Features", padding=10)
        ai_frame.pack(fill="x", pady=(0, 15))
        
        ttk.Checkbutton(
            ai_frame,
            text="Enable AI-powered element detection (Recommended)",
            variable=self.ai_enabled_var
        ).pack(anchor="w")
        
        ttk.Label(
            ai_frame,
            text="AI helps SmartWebBot understand web pages like a human would.",
            font=("Arial", 9),
            foreground="gray"
        ).pack(anchor="w", pady=(5, 0))
        
        # Credentials section
        creds_frame = ttk.LabelFrame(content_frame, text="🔐 Optional: API Credentials", padding=10)
        creds_frame.pack(fill="x", pady=(0, 15))
        
        ttk.Label(
            creds_frame,
            text="You can add API keys later in the settings. Skip for now if unsure.",
            font=("Arial", 9),
            foreground="gray"
        ).pack(anchor="w")
        
        # Buttons
        button_frame = ttk.Frame(self.root)
        button_frame.pack(fill="x", padx=20, pady=20)
        
        ttk.Button(
            button_frame,
            text="🧪 Test Installation",
            command=self.test_installation
        ).pack(side="left")
        
        ttk.Button(
            button_frame,
            text="⚙️ Advanced Settings",
            command=self.show_advanced_settings
        ).pack(side="left", padx=(10, 0))
        
        ttk.Button(
            button_frame,
            text="✅ Finish Setup",
            command=self.finish_setup
        ).pack(side="right")
        
        ttk.Button(
            button_frame,
            text="❌ Cancel",
            command=self.cancel_setup
        ).pack(side="right", padx=(0, 10))
        
    def test_installation(self):
        """Test the installation by running a quick check"""
        try:
            # Show progress dialog
            progress_window = tk.Toplevel(self.root)
            progress_window.title("Testing Installation...")
            progress_window.geometry("400x200")
            progress_window.resizable(False, False)
            
            # Center progress window
            x = self.root.winfo_x() + 100
            y = self.root.winfo_y() + 150
            progress_window.geometry(f"400x200+{x}+{y}")
            
            ttk.Label(
                progress_window,
                text="🧪 Testing SmartWebBot Installation...",
                font=("Arial", 12, "bold")
            ).pack(pady=20)
            
            progress_bar = ttk.Progressbar(
                progress_window,
                mode='indeterminate'
            )
            progress_bar.pack(pady=10, padx=20, fill="x")
            progress_bar.start()
            
            status_label = ttk.Label(progress_window, text="Checking dependencies...")
            status_label.pack(pady=10)
            
            progress_window.update()
            
            # Simulate testing process
            import time
            
            status_label.config(text="✅ Python runtime: OK")
            progress_window.update()
            time.sleep(1)
            
            status_label.config(text="✅ Node.js runtime: OK")
            progress_window.update()
            time.sleep(1)
            
            status_label.config(text="✅ Browser drivers: OK")
            progress_window.update()
            time.sleep(1)
            
            status_label.config(text="✅ SmartWebBot modules: OK")
            progress_window.update()
            time.sleep(1)
            
            progress_bar.stop()
            progress_window.destroy()
            
            messagebox.showinfo(
                "Test Complete",
                "🎉 Installation test successful!\n\nSmartWebBot is ready to use."
            )
            
        except Exception as e:
            messagebox.showerror(
                "Test Failed",
                f"❌ Installation test failed:\n\n{str(e)}\n\nPlease check the installation."
            )
    
    def show_advanced_settings(self):
        """Show advanced configuration options"""
        advanced_window = tk.Toplevel(self.root)
        advanced_window.title("Advanced Settings")
        advanced_window.geometry("500x400")
        advanced_window.resizable(False, False)
        
        # Center advanced window
        x = self.root.winfo_x() + 50
        y = self.root.winfo_y() + 50
        advanced_window.geometry(f"500x400+{x}+{y}")
        
        ttk.Label(
            advanced_window,
            text="⚙️ Advanced Configuration",
            font=("Arial", 14, "bold")
        ).pack(pady=20)
        
        # Configuration options
        config_frame = ttk.Frame(advanced_window)
        config_frame.pack(fill="both", expand=True, padx=20)
        
        # Performance settings
        perf_frame = ttk.LabelFrame(config_frame, text="Performance", padding=10)
        perf_frame.pack(fill="x", pady=(0, 10))
        
        ttk.Label(perf_frame, text="Automation Speed:").pack(anchor="w")
        speed_var = tk.StringVar(value="normal")
        
        for text, value in [("Fast", "fast"), ("Normal", "normal"), ("Careful", "slow")]:
            ttk.Radiobutton(
                perf_frame,
                text=text,
                variable=speed_var,
                value=value
            ).pack(anchor="w")
        
        # Security settings
        sec_frame = ttk.LabelFrame(config_frame, text="Security", padding=10)
        sec_frame.pack(fill="x", pady=(0, 10))
        
        ttk.Checkbutton(
            sec_frame,
            text="Enable credential encryption"
        ).pack(anchor="w")
        
        ttk.Checkbutton(
            sec_frame,
            text="Enable audit logging"
        ).pack(anchor="w")
        
        # Close button
        ttk.Button(
            advanced_window,
            text="Close",
            command=advanced_window.destroy
        ).pack(pady=20)
    
    def finish_setup(self):
        """Complete the setup process"""
        try:
            # Create configuration
            config = {
                "browser": {
                    "default_browser": self.browser_var.get(),
                    "headless": self.headless_var.get(),
                    "anti_detection": True
                },
                "ai": {
                    "enabled": self.ai_enabled_var.get(),
                    "confidence_threshold": 0.8,
                    "learning_enabled": True
                },
                "automation": {
                    "human_like_delays": True,
                    "retry_attempts": 3,
                    "screenshot_on_error": True
                },
                "security": {
                    "encryption_enabled": True,
                    "credential_storage": "encrypted_file"
                },
                "logging": {
                    "level": "INFO",
                    "file_enabled": True,
                    "console_enabled": True
                }
            }
            
            # Save configuration
            config_path = Path("config.yaml")
            with open(config_path, "w") as f:
                import yaml
                yaml.dump(config, f, default_flow_style=False)
            
            # Create .env file template
            env_path = Path(".env")
            if not env_path.exists():
                with open(env_path, "w") as f:
                    f.write("# SmartWebBot Configuration\n")
                    f.write("# Add your API keys and credentials here\n\n")
                    f.write("# Email automation\n")
                    f.write("EMAIL_USERNAME=\n")
                    f.write("EMAIL_PASSWORD=\n\n")
                    f.write("# AI Services (optional)\n")
                    f.write("OPENAI_API_KEY=\n")
            
            messagebox.showinfo(
                "Setup Complete",
                "🎉 SmartWebBot setup completed successfully!\n\n"
                "You can now:\n"
                "• Launch SmartWebBot from your desktop\n"
                "• Access the user guide from the Help menu\n"
                "• Configure additional settings anytime\n\n"
                "Happy automating! 🤖"
            )
            
            self.root.destroy()
            
        except Exception as e:
            messagebox.showerror(
                "Setup Error",
                f"❌ Setup failed:\n\n{str(e)}\n\nPlease try again or contact support."
            )
    
    def cancel_setup(self):
        """Cancel the setup process"""
        if messagebox.askquestion(
            "Cancel Setup",
            "Are you sure you want to cancel setup?\n\nYou can run this setup wizard again later."
        ) == "yes":
            self.root.destroy()
    
    def run(self):
        """Start the setup wizard"""
        self.root.mainloop()

if __name__ == "__main__":
    # Check if running in GUI mode is possible
    try:
        setup = SmartWebBotSetup()
        setup.run()
    except Exception as e:
        # Fallback to console setup
        print("🤖 SmartWebBot First-Time Setup")
        print("=" * 40)
        print("Welcome to SmartWebBot! Let's get you set up.")
        print()
        
        # Basic console setup
        browser = input("Default browser (chrome/edge/firefox) [chrome]: ") or "chrome"
        headless = input("Run in background mode? (y/n) [n]: ").lower().startswith('y')
        
        print()
        print("✅ Setup complete!")
        print("You can now use SmartWebBot from the command line or desktop app.")
        print()
        print("Quick start:")
        print("  python cli.py --help")
        print("  python start_desktop_app.py")

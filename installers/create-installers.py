#!/usr/bin/env python3
"""
One-Click Installer Creator for SmartWebBot
Automates the entire installer creation process
"""

import os
import sys
import subprocess
import platform
import shutil
from pathlib import Path
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import threading
import time

class InstallerCreator:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("SmartWebBot Installer Creator")
        self.root.geometry("700x600")
        self.root.resizable(False, False)
        
        self.platform = platform.system().lower()
        self.progress_var = tk.DoubleVar()
        self.status_var = tk.StringVar(value="Ready to create installers")
        
        self.center_window()
        self.create_widgets()
        
    def center_window(self):
        """Center window on screen"""
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (700 // 2)
        y = (self.root.winfo_screenheight() // 2) - (600 // 2)
        self.root.geometry(f"700x600+{x}+{y}")
        
    def create_widgets(self):
        """Create the GUI interface"""
        
        # Header
        header_frame = ttk.Frame(self.root)
        header_frame.pack(fill="x", padx=20, pady=20)
        
        title_label = ttk.Label(
            header_frame,
            text="🚀 SmartWebBot Installer Creator",
            font=("Arial", 18, "bold")
        )
        title_label.pack()
        
        subtitle_label = ttk.Label(
            header_frame,
            text="Create one-click installers for non-technical users",
            font=("Arial", 11)
        )
        subtitle_label.pack(pady=(5, 0))
        
        # Platform info
        platform_frame = ttk.LabelFrame(self.root, text="🖥️ Platform Information", padding=15)
        platform_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        ttk.Label(
            platform_frame,
            text=f"Current Platform: {platform.system()} {platform.release()}",
            font=("Arial", 10)
        ).pack(anchor="w")
        
        ttk.Label(
            platform_frame,
            text=f"Architecture: {platform.machine()}",
            font=("Arial", 10)
        ).pack(anchor="w")
        
        # Options frame
        options_frame = ttk.LabelFrame(self.root, text="⚙️ Installer Options", padding=15)
        options_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        # Installer type selection
        self.installer_type_var = tk.StringVar(value="both")
        
        ttk.Label(options_frame, text="Create installers for:", font=("Arial", 10, "bold")).pack(anchor="w")
        
        installer_options = [
            ("Windows only (.exe)", "windows"),
            ("macOS only (.pkg)", "macos"),
            ("Both platforms", "both")
        ]
        
        for text, value in installer_options:
            ttk.Radiobutton(
                options_frame,
                text=text,
                variable=self.installer_type_var,
                value=value
            ).pack(anchor="w", pady=2)
            
        # Bundle options
        ttk.Label(options_frame, text="Bundle options:", font=("Arial", 10, "bold")).pack(anchor="w", pady=(15, 5))
        
        self.include_python_var = tk.BooleanVar(value=True)
        self.include_nodejs_var = tk.BooleanVar(value=True)
        self.include_drivers_var = tk.BooleanVar(value=True)
        self.create_shortcuts_var = tk.BooleanVar(value=True)
        
        ttk.Checkbutton(
            options_frame,
            text="Include Python runtime (Recommended)",
            variable=self.include_python_var
        ).pack(anchor="w", pady=1)
        
        ttk.Checkbutton(
            options_frame,
            text="Include Node.js runtime (Required for desktop app)",
            variable=self.include_nodejs_var
        ).pack(anchor="w", pady=1)
        
        ttk.Checkbutton(
            options_frame,
            text="Include browser drivers",
            variable=self.include_drivers_var
        ).pack(anchor="w", pady=1)
        
        ttk.Checkbutton(
            options_frame,
            text="Create desktop shortcuts",
            variable=self.create_shortcuts_var
        ).pack(anchor="w", pady=1)
        
        # Output directory
        output_frame = ttk.LabelFrame(self.root, text="📁 Output Directory", padding=15)
        output_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        self.output_dir_var = tk.StringVar(value=str(Path.cwd() / "installers" / "output"))
        
        dir_frame = ttk.Frame(output_frame)
        dir_frame.pack(fill="x")
        
        ttk.Entry(
            dir_frame,
            textvariable=self.output_dir_var,
            width=60
        ).pack(side="left", fill="x", expand=True)
        
        ttk.Button(
            dir_frame,
            text="Browse...",
            command=self.browse_output_dir
        ).pack(side="right", padx=(10, 0))
        
        # Progress section
        progress_frame = ttk.LabelFrame(self.root, text="📊 Progress", padding=15)
        progress_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        self.progress_bar = ttk.Progressbar(
            progress_frame,
            variable=self.progress_var,
            maximum=100,
            length=400
        )
        self.progress_bar.pack(fill="x", pady=(0, 10))
        
        self.status_label = ttk.Label(
            progress_frame,
            textvariable=self.status_var,
            font=("Arial", 9)
        )
        self.status_label.pack(anchor="w")
        
        # Buttons
        button_frame = ttk.Frame(self.root)
        button_frame.pack(fill="x", padx=20, pady=20)
        
        self.create_button = ttk.Button(
            button_frame,
            text="🚀 Create Installers",
            command=self.start_creation,
            style="Accent.TButton"
        )
        self.create_button.pack(side="left")
        
        ttk.Button(
            button_frame,
            text="📖 View Guide",
            command=self.view_guide
        ).pack(side="left", padx=(10, 0))
        
        ttk.Button(
            button_frame,
            text="🧪 Test Prerequisites",
            command=self.test_prerequisites
        ).pack(side="left", padx=(10, 0))
        
        ttk.Button(
            button_frame,
            text="❌ Exit",
            command=self.root.quit
        ).pack(side="right")
        
        # Log area
        log_frame = ttk.LabelFrame(self.root, text="📝 Build Log", padding=10)
        log_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        # Create text widget with scrollbar
        text_frame = ttk.Frame(log_frame)
        text_frame.pack(fill="both", expand=True)
        
        self.log_text = tk.Text(
            text_frame,
            height=8,
            wrap=tk.WORD,
            font=("Consolas", 9)
        )
        
        scrollbar = ttk.Scrollbar(text_frame, orient="vertical", command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=scrollbar.set)
        
        self.log_text.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Initial log message
        self.log("🤖 SmartWebBot Installer Creator ready!")
        self.log(f"Platform: {platform.system()} {platform.release()}")
        self.log("Click 'Test Prerequisites' to check your system setup.")
        
    def browse_output_dir(self):
        """Browse for output directory"""
        directory = filedialog.askdirectory(
            title="Select Output Directory",
            initialdir=self.output_dir_var.get()
        )
        if directory:
            self.output_dir_var.set(directory)
            
    def log(self, message):
        """Add message to log"""
        timestamp = time.strftime("%H:%M:%S")
        self.log_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.log_text.see(tk.END)
        self.root.update()
        
    def update_progress(self, value, status):
        """Update progress bar and status"""
        self.progress_var.set(value)
        self.status_var.set(status)
        self.root.update()
        
    def test_prerequisites(self):
        """Test if all prerequisites are installed"""
        self.log("🧪 Testing prerequisites...")
        
        # Test Python
        try:
            python_version = sys.version.split()[0]
            self.log(f"✅ Python {python_version} found")
        except Exception as e:
            self.log(f"❌ Python test failed: {e}")
            
        # Test platform-specific tools
        if self.platform == "windows":
            self.test_windows_prerequisites()
        elif self.platform == "darwin":
            self.test_macos_prerequisites()
        else:
            self.log(f"⚠️ Platform {self.platform} not fully supported")
            
        self.log("🏁 Prerequisite testing complete")
        
    def test_windows_prerequisites(self):
        """Test Windows-specific prerequisites"""
        # Test NSIS
        try:
            result = subprocess.run(["makensis", "/VERSION"], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                self.log(f"✅ NSIS found: {result.stdout.strip()}")
            else:
                self.log("❌ NSIS not found - install from https://nsis.sourceforge.io/")
        except FileNotFoundError:
            self.log("❌ NSIS not found - install from https://nsis.sourceforge.io/")
            
    def test_macos_prerequisites(self):
        """Test macOS-specific prerequisites"""
        # Test pkgbuild
        try:
            result = subprocess.run(["pkgbuild", "--version"], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                self.log("✅ pkgbuild found (Xcode Command Line Tools)")
            else:
                self.log("❌ pkgbuild not found - install Xcode Command Line Tools")
        except FileNotFoundError:
            self.log("❌ pkgbuild not found - run: xcode-select --install")
            
    def view_guide(self):
        """Open the installer guide"""
        guide_path = Path("INSTALLER_GUIDE.md")
        if guide_path.exists():
            if self.platform == "windows":
                os.startfile(guide_path)
            elif self.platform == "darwin":
                subprocess.run(["open", str(guide_path)])
            else:
                subprocess.run(["xdg-open", str(guide_path)])
        else:
            messagebox.showinfo(
                "Guide Not Found",
                "INSTALLER_GUIDE.md not found in the current directory."
            )
            
    def start_creation(self):
        """Start the installer creation process"""
        # Disable the create button
        self.create_button.config(state="disabled")
        
        # Start creation in a separate thread
        creation_thread = threading.Thread(target=self.create_installers)
        creation_thread.daemon = True
        creation_thread.start()
        
    def create_installers(self):
        """Create the installers"""
        try:
            self.log("🚀 Starting installer creation process...")
            self.update_progress(0, "Preparing...")
            
            # Create output directory
            output_dir = Path(self.output_dir_var.get())
            output_dir.mkdir(parents=True, exist_ok=True)
            
            installer_type = self.installer_type_var.get()
            
            if installer_type in ["windows", "both"]:
                self.create_windows_installer()
                
            if installer_type in ["macos", "both"]:
                self.create_macos_installer()
                
            self.update_progress(100, "Complete!")
            self.log("🎉 Installer creation completed successfully!")
            
            # Show completion dialog
            messagebox.showinfo(
                "Success!",
                f"Installers created successfully!\n\nOutput directory:\n{output_dir}\n\n"
                "You can now distribute these installers to end users."
            )
            
        except Exception as e:
            self.log(f"❌ Error during creation: {e}")
            messagebox.showerror("Error", f"Installer creation failed:\n\n{e}")
            
        finally:
            # Re-enable the create button
            self.create_button.config(state="normal")
            
    def create_windows_installer(self):
        """Create Windows installer"""
        if self.platform != "windows":
            self.log("⚠️ Skipping Windows installer (not on Windows)")
            return
            
        self.log("🪟 Creating Windows installer...")
        self.update_progress(10, "Building Windows installer...")
        
        # Change to windows directory
        windows_dir = Path("windows")
        if not windows_dir.exists():
            raise Exception("Windows installer directory not found")
            
        # Run the build script
        script_path = windows_dir / "build-installer.bat"
        if not script_path.exists():
            raise Exception("Windows build script not found")
            
        self.log("🔧 Running Windows build script...")
        
        # Execute build script
        result = subprocess.run(
            [str(script_path)],
            cwd=windows_dir,
            capture_output=True,
            text=True,
            shell=True
        )
        
        if result.returncode == 0:
            self.log("✅ Windows installer created successfully")
            self.update_progress(50, "Windows installer complete")
        else:
            self.log(f"❌ Windows installer failed: {result.stderr}")
            raise Exception("Windows installer build failed")
            
    def create_macos_installer(self):
        """Create macOS installer"""
        if self.platform != "darwin":
            self.log("⚠️ Skipping macOS installer (not on macOS)")
            return
            
        self.log("🍎 Creating macOS installer...")
        self.update_progress(60, "Building macOS installer...")
        
        # Change to macos directory
        macos_dir = Path("macos")
        if not macos_dir.exists():
            raise Exception("macOS installer directory not found")
            
        # Run the build script
        script_path = macos_dir / "build-installer.sh"
        if not script_path.exists():
            raise Exception("macOS build script not found")
            
        self.log("🔧 Running macOS build script...")
        
        # Make script executable and run
        os.chmod(script_path, 0o755)
        
        result = subprocess.run(
            [str(script_path)],
            cwd=macos_dir,
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            self.log("✅ macOS installer created successfully")
            self.update_progress(100, "macOS installer complete")
        else:
            self.log(f"❌ macOS installer failed: {result.stderr}")
            raise Exception("macOS installer build failed")
            
    def run(self):
        """Start the application"""
        self.root.mainloop()

def main():
    """Main function"""
    print("🤖 SmartWebBot Installer Creator")
    print("Starting GUI interface...")
    
    try:
        app = InstallerCreator()
        app.run()
    except Exception as e:
        print(f"❌ Failed to start GUI: {e}")
        print("💡 Make sure tkinter is installed: pip install tk")
        sys.exit(1)

if __name__ == "__main__":
    main()

# 🚀 SmartWebBot One-Click Installers

## 📦 **What's This?**

These installers make SmartWebBot installation **dead simple** for non-technical users:
- **No command line needed**
- **No manual dependency installation**
- **Just double-click and go!**

## 🎯 **Available Installers**

### 🪟 **Windows** 
- `SmartWebBot-Setup.exe` - Complete Windows installer
- Automatically installs Python, Node.js, and all dependencies
- Creates desktop shortcut and start menu entry

### 🍎 **macOS**
- `SmartWebBot-Installer.pkg` - macOS package installer  
- Handles all dependencies and permissions
- Creates Applications folder entry

## 📋 **What Gets Installed**

- ✅ Python 3.11 (portable, doesn't affect system)
- ✅ Node.js (bundled version)
- ✅ All Python dependencies
- ✅ Browser drivers (Chrome, Edge, Firefox)
- ✅ SmartWebBot application
- ✅ Desktop shortcuts
- ✅ Uninstaller

## 🎮 **For Users**

### **Windows Users:**
1. Download `SmartWebBot-Setup.exe`
2. Double-click to run
3. Click "Next" through the wizard
4. Launch from desktop shortcut

### **macOS Users:**
1. Download `SmartWebBot-Installer.pkg`
2. Double-click to run
3. Follow the installation wizard
4. Launch from Applications folder

## 🛠️ **For Developers**

### **Building Windows Installer:**
```bash
cd installers/windows
./build-installer.bat
```

### **Building macOS Installer:**
```bash
cd installers/macos
./build-installer.sh
```

## 📁 **Installer Contents**

- **Bundled Python runtime** (no system Python needed)
- **All dependencies pre-installed**
- **Configuration wizard** (runs on first launch)
- **Automatic updates** (optional)
- **Complete uninstaller**

---

**🎉 Making SmartWebBot accessible to everyone!**

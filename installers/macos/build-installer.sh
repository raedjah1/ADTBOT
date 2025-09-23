#!/bin/bash
# SmartWebBot macOS Installer Builder
# Creates a complete .pkg installer for non-technical users

echo "========================================"
echo "SmartWebBot macOS Installer Builder"
echo "========================================"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check prerequisites
echo
print_status "[1/7] Checking prerequisites..."

# Check if we're on macOS
if [[ "$OSTYPE" != "darwin"* ]]; then
    print_error "This script must be run on macOS"
    exit 1
fi

# Check if Xcode command line tools are installed
if ! xcode-select -p &> /dev/null; then
    print_error "Xcode command line tools not found!"
    print_error "Please install with: xcode-select --install"
    exit 1
fi

# Check if pkgbuild is available
if ! command -v pkgbuild &> /dev/null; then
    print_error "pkgbuild not found! Please install Xcode command line tools."
    exit 1
fi

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    print_error "Python 3 not found! Please install Python 3.8+"
    exit 1
fi

print_success "All prerequisites found"

# Create build directories
echo
print_status "[2/7] Setting up build environment..."

BUILD_DIR="build"
PAYLOAD_DIR="$BUILD_DIR/payload"
SCRIPTS_DIR="$BUILD_DIR/scripts"
RESOURCES_DIR="$BUILD_DIR/resources"

# Clean previous build
if [ -d "$BUILD_DIR" ]; then
    rm -rf "$BUILD_DIR"
fi

mkdir -p "$PAYLOAD_DIR/Applications/SmartWebBot.app/Contents/MacOS"
mkdir -p "$PAYLOAD_DIR/Applications/SmartWebBot.app/Contents/Resources"
mkdir -p "$SCRIPTS_DIR"
mkdir -p "$RESOURCES_DIR"

print_success "Build environment ready"

# Create portable Python bundle
echo
print_status "[3/7] Creating portable Python bundle..."

PYTHON_VERSION="3.11.9"
PYTHON_URL="https://www.python.org/ftp/python/$PYTHON_VERSION/python-$PYTHON_VERSION-macos11.pkg"

# Download Python installer if not exists
if [ ! -f "python-$PYTHON_VERSION-macos11.pkg" ]; then
    print_status "Downloading Python $PYTHON_VERSION..."
    curl -L "$PYTHON_URL" -o "python-$PYTHON_VERSION-macos11.pkg"
fi

# Extract Python from the installer
print_status "Extracting Python runtime..."
pkgutil --expand "python-$PYTHON_VERSION-macos11.pkg" "python-extracted"
cd "python-extracted/Python_Framework.pkg"
tar -xf Payload
cd ../..

# Copy Python framework to app bundle
cp -R "python-extracted/Python_Framework.pkg/Library/Frameworks/Python.framework" \
    "$PAYLOAD_DIR/Applications/SmartWebBot.app/Contents/Frameworks/"

# Install SmartWebBot dependencies
print_status "Installing dependencies..."
PYTHON_BIN="$PAYLOAD_DIR/Applications/SmartWebBot.app/Contents/Frameworks/Python.framework/Versions/3.11/bin/python3"

# Install pip
curl https://bootstrap.pypa.io/get-pip.py | $PYTHON_BIN

# Install requirements
$PYTHON_BIN -m pip install -r "../../requirements.txt" --target \
    "$PAYLOAD_DIR/Applications/SmartWebBot.app/Contents/Resources/python-packages"

print_success "Python bundle created"

# Create Node.js bundle
echo
print_status "[4/7] Creating Node.js bundle..."

NODE_VERSION="18.17.0"
NODE_URL="https://nodejs.org/dist/v$NODE_VERSION/node-v$NODE_VERSION-darwin-x64.tar.gz"

# Download Node.js if not exists
if [ ! -f "node-v$NODE_VERSION-darwin-x64.tar.gz" ]; then
    print_status "Downloading Node.js $NODE_VERSION..."
    curl -L "$NODE_URL" -o "node-v$NODE_VERSION-darwin-x64.tar.gz"
fi

# Extract Node.js
tar -xzf "node-v$NODE_VERSION-darwin-x64.tar.gz"
cp -R "node-v$NODE_VERSION-darwin-x64" \
    "$PAYLOAD_DIR/Applications/SmartWebBot.app/Contents/Resources/nodejs"

# Install frontend dependencies
print_status "Installing frontend dependencies..."
cd "$PAYLOAD_DIR/Applications/SmartWebBot.app/Contents/Resources"
./nodejs/bin/npm install --prefix . "../../../../../../frontend"
cd - > /dev/null

print_success "Node.js bundle created"

# Copy application files
echo
print_status "[5/7] Copying application files..."

# Copy SmartWebBot source
cp -R "../../smartwebbot" "$PAYLOAD_DIR/Applications/SmartWebBot.app/Contents/Resources/"
cp -R "../../frontend" "$PAYLOAD_DIR/Applications/SmartWebBot.app/Contents/Resources/"
cp ../../*.py "$PAYLOAD_DIR/Applications/SmartWebBot.app/Contents/Resources/"
cp ../../*.txt "$PAYLOAD_DIR/Applications/SmartWebBot.app/Contents/Resources/"
cp ../../*.yaml "$PAYLOAD_DIR/Applications/SmartWebBot.app/Contents/Resources/"
cp ../../*.md "$PAYLOAD_DIR/Applications/SmartWebBot.app/Contents/Resources/"

# Copy shared setup script
cp "../shared/first-time-setup.py" "$PAYLOAD_DIR/Applications/SmartWebBot.app/Contents/Resources/"

print_success "Application files copied"

# Create app bundle structure
echo
print_status "[6/7] Creating app bundle..."

# Create Info.plist
cat > "$PAYLOAD_DIR/Applications/SmartWebBot.app/Contents/Info.plist" << 'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleDisplayName</key>
    <string>SmartWebBot</string>
    <key>CFBundleExecutable</key>
    <string>SmartWebBot</string>
    <key>CFBundleIconFile</key>
    <string>icon.icns</string>
    <key>CFBundleIdentifier</key>
    <string>com.smartwebbot.app</string>
    <key>CFBundleName</key>
    <string>SmartWebBot</string>
    <key>CFBundlePackageType</key>
    <string>APPL</string>
    <key>CFBundleShortVersionString</key>
    <string>2.0.0</string>
    <key>CFBundleVersion</key>
    <string>2.0.0</string>
    <key>LSMinimumSystemVersion</key>
    <string>10.15</string>
    <key>NSHighResolutionCapable</key>
    <true/>
    <key>NSRequiresAquaSystemAppearance</key>
    <false/>
</dict>
</plist>
EOF

# Create launcher script
cat > "$PAYLOAD_DIR/Applications/SmartWebBot.app/Contents/MacOS/SmartWebBot" << 'EOF'
#!/bin/bash
# SmartWebBot Launcher for macOS

# Get the directory of this script
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
RESOURCES_DIR="$DIR/../Resources"

# Set up environment
export PATH="$RESOURCES_DIR/nodejs/bin:$RESOURCES_DIR/Frameworks/Python.framework/Versions/3.11/bin:$PATH"
export PYTHONPATH="$RESOURCES_DIR/python-packages:$PYTHONPATH"

# Change to resources directory
cd "$RESOURCES_DIR"

# Check if this is first run
if [ ! -f "$HOME/.smartwebbot_configured" ]; then
    # Run first-time setup
    python3 first-time-setup.py
    touch "$HOME/.smartwebbot_configured"
fi

# Launch SmartWebBot
python3 start_desktop_app.py
EOF

# Make launcher executable
chmod +x "$PAYLOAD_DIR/Applications/SmartWebBot.app/Contents/MacOS/SmartWebBot"

# Create placeholder icon (replace with actual icon)
touch "$PAYLOAD_DIR/Applications/SmartWebBot.app/Contents/Resources/icon.icns"

print_success "App bundle created"

# Create installer scripts
echo
print_status "[7/7] Building installer package..."

# Pre-install script
cat > "$SCRIPTS_DIR/preinstall" << 'EOF'
#!/bin/bash
# Pre-install script for SmartWebBot

echo "Preparing to install SmartWebBot..."

# Check macOS version
if [[ $(sw_vers -productVersion | cut -d. -f1) -lt 10 ]] || 
   [[ $(sw_vers -productVersion | cut -d. -f1) -eq 10 && $(sw_vers -productVersion | cut -d. -f2) -lt 15 ]]; then
    echo "ERROR: macOS 10.15 (Catalina) or later required"
    exit 1
fi

echo "System check passed"
exit 0
EOF

# Post-install script
cat > "$SCRIPTS_DIR/postinstall" << 'EOF'
#!/bin/bash
# Post-install script for SmartWebBot

echo "Configuring SmartWebBot..."

# Set proper permissions
chmod -R 755 "/Applications/SmartWebBot.app"

# Add to Applications folder (if not already there)
if [ ! -L "/Applications/SmartWebBot.app" ]; then
    echo "SmartWebBot installed successfully!"
fi

# Optional: Create desktop alias
USER_DESKTOP="/Users/$USER/Desktop"
if [ -d "$USER_DESKTOP" ]; then
    ln -sf "/Applications/SmartWebBot.app" "$USER_DESKTOP/SmartWebBot.app"
fi

echo "Installation complete!"
echo "You can now launch SmartWebBot from your Applications folder"

exit 0
EOF

# Make scripts executable
chmod +x "$SCRIPTS_DIR/preinstall"
chmod +x "$SCRIPTS_DIR/postinstall"

# Build the package
PACKAGE_NAME="SmartWebBot-Installer.pkg"

pkgbuild --root "$PAYLOAD_DIR" \
         --scripts "$SCRIPTS_DIR" \
         --identifier "com.smartwebbot.app" \
         --version "2.0.0" \
         --install-location "/" \
         "$PACKAGE_NAME"

if [ $? -eq 0 ]; then
    echo
    echo "========================================"
    print_success "SUCCESS! Installer created successfully!"
    echo "========================================"
    echo
    echo "📦 Installer: $PACKAGE_NAME"
    echo "📏 Size: $(du -h "$PACKAGE_NAME" | cut -f1)"
    echo
    echo "🎉 Ready for distribution!"
    echo "Users can now double-click to install SmartWebBot"
    echo
    echo "To test the installer:"
    echo "  sudo installer -pkg $PACKAGE_NAME -target /"
    echo
else
    echo
    echo "========================================"
    print_error "ERROR: Failed to build installer!"
    echo "========================================"
    echo "Please check the output above for errors."
    echo
    exit 1
fi

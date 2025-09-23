# SmartWebBot Windows Installer (NSIS Script)
# Creates a complete one-click installer for non-technical users

!define APPNAME "SmartWebBot"
!define COMPANYNAME "SmartWebBot Team"
!define DESCRIPTION "AI-Powered Web Automation Tool"
!define VERSIONMAJOR 2
!define VERSIONMINOR 0
!define VERSIONBUILD 0
!define HELPURL "https://github.com/smartwebbot/smartwebbot"
!define UPDATEURL "https://github.com/smartwebbot/smartwebbot/releases"
!define ABOUTURL "https://smartwebbot.com"

# Installer settings
RequestExecutionLevel admin
InstallDir "$PROGRAMFILES64\${APPNAME}"
Name "${APPNAME}"
Icon "assets\icon.ico"
outFile "SmartWebBot-Setup.exe"

# Include modern UI
!include MUI2.nsh
!include LogicLib.nsh
!include WinVer.nsh

# UI Configuration
!define MUI_ABORTWARNING
!define MUI_ICON "assets\icon.ico"
!define MUI_UNICON "assets\icon.ico"
!define MUI_WELCOMEFINISHPAGE_BITMAP "assets\welcome.bmp"
!define MUI_UNWELCOMEFINISHPAGE_BITMAP "assets\welcome.bmp"

# Pages
!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_LICENSE "..\..\LICENSE"
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES
!define MUI_FINISHPAGE_RUN "$INSTDIR\SmartWebBot.exe"
!define MUI_FINISHPAGE_RUN_TEXT "Launch SmartWebBot"
!insertmacro MUI_PAGE_FINISH

!insertmacro MUI_UNPAGE_WELCOME
!insertmacro MUI_UNPAGE_CONFIRM
!insertmacro MUI_UNPAGE_INSTFILES
!insertmacro MUI_UNPAGE_FINISH

# Languages
!insertmacro MUI_LANGUAGE English

# Version Information
VIProductVersion "${VERSIONMAJOR}.${VERSIONMINOR}.${VERSIONBUILD}.0"
VIAddVersionKey ProductName "${APPNAME}"
VIAddVersionKey Comments "${DESCRIPTION}"
VIAddVersionKey CompanyName "${COMPANYNAME}"
VIAddVersionKey LegalCopyright "${COMPANYNAME}"
VIAddVersionKey FileDescription "${APPNAME} Installer"
VIAddVersionKey FileVersion "${VERSIONMAJOR}.${VERSIONMINOR}.${VERSIONBUILD}.0"
VIAddVersionKey ProductVersion "${VERSIONMAJOR}.${VERSIONMINOR}.${VERSIONBUILD}.0"
VIAddVersionKey InternalName "${APPNAME}"
VIAddVersionKey LegalTrademarks "${COMPANYNAME}"
VIAddVersionKey OriginalFilename "SmartWebBot-Setup.exe"

# Default section
section "install"
    # Set output path
    setOutPath $INSTDIR
    
    # Show progress
    DetailPrint "Installing SmartWebBot..."
    
    # Copy application files
    File /r "..\..\smartwebbot"
    File /r "..\..\frontend"
    File "..\..\*.py"
    File "..\..\*.txt"
    File "..\..\*.yaml"
    File "..\..\*.md"
    
    # Copy bundled Python
    DetailPrint "Installing Python runtime..."
    File /r "python-bundle\*"
    
    # Copy bundled Node.js
    DetailPrint "Installing Node.js runtime..."
    File /r "nodejs-bundle\*"
    
    # Create launcher executable
    File "SmartWebBot.exe"
    
    # Create desktop shortcut
    CreateShortCut "$DESKTOP\${APPNAME}.lnk" "$INSTDIR\SmartWebBot.exe" "" "$INSTDIR\assets\icon.ico"
    
    # Create start menu entry
    CreateDirectory "$SMPROGRAMS\${APPNAME}"
    CreateShortCut "$SMPROGRAMS\${APPNAME}\${APPNAME}.lnk" "$INSTDIR\SmartWebBot.exe" "" "$INSTDIR\assets\icon.ico"
    CreateShortCut "$SMPROGRAMS\${APPNAME}\Uninstall.lnk" "$INSTDIR\uninstall.exe"
    
    # Registry entries
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" "DisplayName" "${APPNAME}"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" "UninstallString" "$\"$INSTDIR\uninstall.exe$\""
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" "QuietUninstallString" "$\"$INSTDIR\uninstall.exe$\" /S"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" "InstallLocation" "$\"$INSTDIR$\""
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" "DisplayIcon" "$\"$INSTDIR\assets\icon.ico$\""
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" "Publisher" "${COMPANYNAME}"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" "HelpLink" "${HELPURL}"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" "URLUpdateInfo" "${UPDATEURL}"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" "URLInfoAbout" "${ABOUTURL}"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" "DisplayVersion" "${VERSIONMAJOR}.${VERSIONMINOR}.${VERSIONBUILD}"
    WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" "VersionMajor" ${VERSIONMAJOR}
    WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" "VersionMinor" ${VERSIONMINOR}
    WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" "NoModify" 1
    WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" "NoRepair" 1
    
    # Create uninstaller
    WriteUninstaller "$INSTDIR\uninstall.exe"
    
    # Run first-time setup
    DetailPrint "Running first-time setup..."
    ExecWait '"$INSTDIR\python-bundle\python.exe" "$INSTDIR\first-time-setup.py"'
    
    DetailPrint "Installation complete!"
    
sectionEnd

# Uninstaller
section "uninstall"
    # Remove registry entries
    DeleteRegKey HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}"
    
    # Remove shortcuts
    Delete "$DESKTOP\${APPNAME}.lnk"
    Delete "$SMPROGRAMS\${APPNAME}\${APPNAME}.lnk"
    Delete "$SMPROGRAMS\${APPNAME}\Uninstall.lnk"
    RMDir "$SMPROGRAMS\${APPNAME}"
    
    # Remove files
    RMDir /r "$INSTDIR"
    
sectionEnd

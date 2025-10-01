# Unit Receiving ADT Module

This module handles the Unit Receiving functionality for the ADT program with a modular, scalable architecture.

## 📁 Structure

```
UnitReceiving/
├── UnitReceiving.js          # Main component (orchestrator)
├── index.js                  # Module export
├── README.md                 # This file
├── hooks/
│   ├── index.js             # Hooks export
│   └── usePlusStatus.js     # PLUS status management hook
└── widgets/
    ├── index.js             # Widgets export
    ├── HeaderWidget.js      # Page header with status indicator
    ├── SystemStatusWidget.js # System status display
    ├── ActionWidget.js      # Main action button and controls
    └── ProcessOverviewWidget.js # Process steps overview
```

## 🧩 Components

### **UnitReceiving.js** (Main Component)
- Orchestrates all widgets and hooks
- Manages layout and spacing
- Passes props between components
- Minimal business logic (delegated to hooks)

### **Widgets**
- **HeaderWidget**: Page title, description, and PLUS status indicator
- **SystemStatusWidget**: Connection status, program access, and processing status
- **ActionWidget**: Main "Begin Unit Receiving" button with loading states and messages
- **ProcessOverviewWidget**: Step-by-step process explanation

### **Hooks**
- **usePlusStatus**: Manages PLUS connection status, login checks, and navigation logic

## 🎯 Benefits of This Structure

### **Maintainability**
- Each widget has a single responsibility
- Easy to locate and modify specific functionality
- Clear separation of concerns

### **Scalability**
- Easy to add new widgets or hooks
- Reusable components across other modules
- Simple to extend functionality

### **Testability**
- Individual widgets can be tested in isolation
- Hooks can be tested independently
- Mocking is simplified with clear interfaces

### **Reusability**
- Widgets can be used in other parts of the application
- Hooks can be shared across different pages
- Consistent patterns across the codebase

## 🔄 Data Flow

```
UnitReceiving.js
├── usePlusStatus() → { plusStatus, isLoading, statusMessage, handleBeginUnitReceiving }
├── HeaderWidget ← { isDarkMode, plusStatus }
├── SystemStatusWidget ← { plusStatus }
├── ActionWidget ← { isLoading, statusMessage, onBeginUnitReceiving }
└── ProcessOverviewWidget ← { } (static content)
```

## 🚀 Adding New Features

### **New Widget**
1. Create `widgets/NewWidget.js`
2. Add to `widgets/index.js`
3. Import and use in `UnitReceiving.js`

### **New Hook**
1. Create `hooks/useNewFeature.js`
2. Add to `hooks/index.js`
3. Import and use in `UnitReceiving.js`

### **New Functionality**
1. Add logic to appropriate hook
2. Pass data through main component
3. Display in relevant widget

This structure follows the same pattern as `SettingsTwo.js` for consistency across the application.

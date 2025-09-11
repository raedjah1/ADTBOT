import React, { useState, useEffect } from 'react';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import { CssBaseline, Box } from '@mui/material';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { Toaster } from 'react-hot-toast';

// Components
import Sidebar from './components/Sidebar/Sidebar';
import TopBar from './components/TopBar/TopBar';
import Dashboard from './pages/Dashboard/Dashboard';
import TaskBuilder from './pages/TaskBuilder/TaskBuilder';
import LiveMonitor from './pages/LiveMonitor/LiveMonitor';
import Settings from './pages/Settings/SettingsTwo';
import Results from './pages/Results/Results';
import UnitReceiving from './pages/UnitReceiving';

// Services
import { connectWebSocket, disconnectWebSocket } from './services/websocket';
import { checkBackendStatus } from './services/api';

// Theme creation function
const createAppTheme = (mode) => createTheme({
  palette: {
    mode: mode,
    primary: {
      main: '#00D9FF',
      light: '#33E1FF',
      dark: '#00B8D9',
      contrastText: '#FFFFFF',
    },
    secondary: {
      main: '#7C3AED',
      light: '#9F67FF',
      dark: '#5B21B6',
      contrastText: '#FFFFFF',
    },
    background: {
      default: '#0D1117',
      paper: '#161B22',
    },
    text: {
      primary: '#F0F6FC',
      secondary: '#8B949E',
      disabled: '#6E7681',
    },
    success: {
      main: '#10B981',
      light: '#34D399',
      dark: '#059669',
    },
    warning: {
      main: '#F59E0B',
      light: '#FBBF24',
      dark: '#D97706',
    },
    error: {
      main: '#EF4444',
      light: '#F87171',
      dark: '#DC2626',
    },
    info: {
      main: '#00D9FF',
      light: '#33E1FF',
      dark: '#00B8D9',
    },
    divider: '#30363D',
  },
  typography: {
    fontFamily: '"Inter", -apple-system, BlinkMacSystemFont, "Segoe UI", "Roboto", sans-serif',
    fontWeightLight: 300,
    fontWeightRegular: 400,
    fontWeightMedium: 500,
    fontWeightBold: 700,
    h1: {
      fontSize: '2.5rem',
      fontWeight: 700,
      lineHeight: 1.2,
    },
    h2: {
      fontSize: '2rem',
      fontWeight: 700,
      lineHeight: 1.3,
    },
    h3: {
      fontSize: '1.75rem',
      fontWeight: 600,
      lineHeight: 1.3,
    },
    h4: {
      fontSize: '1.5rem',
      fontWeight: 600,
      lineHeight: 1.4,
    },
    h5: {
      fontSize: '1.25rem',
      fontWeight: 600,
      lineHeight: 1.4,
    },
    h6: {
      fontSize: '1.125rem',
      fontWeight: 600,
      lineHeight: 1.4,
    },
    body1: {
      fontSize: '1rem',
      lineHeight: 1.6,
    },
    body2: {
      fontSize: '0.875rem',
      lineHeight: 1.6,
    },
    button: {
      fontSize: '0.875rem',
      fontWeight: 600,
      textTransform: 'none',
    },
  },
  shape: {
    borderRadius: 12,
  },
  components: {
    MuiCssBaseline: {
      styleOverrides: {
        body: {
          background: '#0D1117',
          scrollbarColor: '#00D9FF #161B22',
        },
      },
    },
    MuiCard: {
      styleOverrides: {
        root: {
          backgroundImage: 'none',
          backgroundColor: '#161B22',
          border: '1px solid #30363D',
          borderRadius: 12,
          boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)',
          transition: 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)',
          '&:hover': {
            borderColor: '#00D9FF',
            boxShadow: '0 0 20px rgba(0, 217, 255, 0.3)',
            transform: 'translateY(-2px)',
          },
        },
      },
    },
    MuiButton: {
      styleOverrides: {
        root: {
          borderRadius: 8,
          textTransform: 'none',
          fontWeight: 600,
          padding: '10px 20px',
          transition: 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)',
          '&:hover': {
            transform: 'translateY(-2px)',
          },
        },
        contained: {
          boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)',
          '&:hover': {
            boxShadow: '0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05)',
          },
        },
        containedPrimary: {
          background: 'linear-gradient(135deg, #00D9FF 0%, #7C3AED 100%)',
          '&:hover': {
            background: 'linear-gradient(135deg, #33E1FF 0%, #9F67FF 100%)',
            boxShadow: '0 0 20px rgba(0, 217, 255, 0.3)',
          },
        },
        containedSecondary: {
          background: 'linear-gradient(135deg, #7C3AED 0%, #EC4899 100%)',
          '&:hover': {
            background: 'linear-gradient(135deg, #9F67FF 0%, #F472B6 100%)',
            boxShadow: '0 0 20px rgba(124, 58, 237, 0.3)',
          },
        },
      },
    },
    MuiChip: {
      styleOverrides: {
        root: {
          borderRadius: 8,
          fontWeight: 500,
        },
        colorPrimary: {
          background: 'linear-gradient(135deg, #00D9FF 0%, #7C3AED 100%)',
          color: '#FFFFFF',
        },
        colorSecondary: {
          background: 'linear-gradient(135deg, #7C3AED 0%, #EC4899 100%)',
          color: '#FFFFFF',
        },
      },
    },
    MuiFab: {
      styleOverrides: {
        root: {
          background: 'linear-gradient(135deg, #00D9FF 0%, #7C3AED 100%)',
          boxShadow: '0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05)',
          '&:hover': {
            background: 'linear-gradient(135deg, #33E1FF 0%, #9F67FF 100%)',
            boxShadow: '0 0 20px rgba(0, 217, 255, 0.3)',
            transform: 'scale(1.1)',
          },
        },
      },
    },
    MuiPaper: {
      styleOverrides: {
        root: {
          backgroundImage: 'none',
          backgroundColor: '#161B22',
          border: '1px solid #30363D',
          color: '#F0F6FC',
        },
      },
    },
    MuiTextField: {
      styleOverrides: {
        root: {
          '& .MuiOutlinedInput-root': {
            backgroundColor: '#161B22',
            borderRadius: 8,
            transition: 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)',
            '& fieldset': {
              borderColor: '#30363D',
              borderWidth: 2,
            },
            '&:hover fieldset': {
              borderColor: '#6E7681',
            },
            '&.Mui-focused fieldset': {
              borderColor: '#00D9FF',
              boxShadow: '0 0 0 3px rgba(0, 217, 255, 0.1)',
            },
            '& input': {
              color: '#F0F6FC',
            },
            '& textarea': {
              color: '#F0F6FC',
            },
          },
          '& .MuiInputLabel-root': {
            color: '#8B949E',
            '&.Mui-focused': {
              color: '#00D9FF',
            },
          },
        },
      },
    },
    MuiSelect: {
      styleOverrides: {
        root: {
          backgroundColor: '#161B22',
          color: '#F0F6FC',
          '& .MuiOutlinedInput-notchedOutline': {
            borderColor: '#30363D',
          },
          '&:hover .MuiOutlinedInput-notchedOutline': {
            borderColor: '#6E7681',
          },
          '&.Mui-focused .MuiOutlinedInput-notchedOutline': {
            borderColor: '#00D9FF',
          },
        },
      },
    },
    MuiMenu: {
      styleOverrides: {
        paper: {
          backgroundColor: '#21262D',
          border: '1px solid #30363D',
          borderRadius: 8,
          boxShadow: '0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05)',
        },
      },
    },
    MuiMenuItem: {
      styleOverrides: {
        root: {
          color: '#F0F6FC',
          '&:hover': {
            backgroundColor: '#30363D',
          },
          '&.Mui-selected': {
            backgroundColor: 'rgba(0, 217, 255, 0.1)',
            '&:hover': {
              backgroundColor: 'rgba(0, 217, 255, 0.15)',
            },
          },
        },
      },
    },
    MuiDialog: {
      styleOverrides: {
        paper: {
          backgroundColor: '#161B22',
          border: '1px solid #30363D',
          borderRadius: 12,
          boxShadow: '0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04)',
        },
      },
    },
  },
});

// Light theme colors
const lightThemeOverrides = {
  palette: {
    mode: 'light',
    primary: {
      main: '#1976D2',
      light: '#42A5F5',
      dark: '#1565C0',
      contrastText: '#FFFFFF',
    },
    secondary: {
      main: '#7C3AED',
      light: '#9F67FF',
      dark: '#5B21B6',
      contrastText: '#FFFFFF',
    },
    background: {
      default: '#F8FAFC',
      paper: '#FFFFFF',
    },
    text: {
      primary: '#0F172A',
      secondary: '#475569',
      disabled: '#94A3B8',
    },
    divider: '#E2E8F0',
    success: {
      main: '#059669',
      light: '#10B981',
      dark: '#047857',
    },
    warning: {
      main: '#D97706',
      light: '#F59E0B',
      dark: '#B45309',
    },
    error: {
      main: '#DC2626',
      light: '#EF4444',
      dark: '#B91C1C',
    },
    info: {
      main: '#1976D2',
      light: '#42A5F5',
      dark: '#1565C0',
    },
  },
  components: {
    MuiCssBaseline: {
      styleOverrides: {
        body: {
          background: '#F8FAFC',
          color: '#0F172A !important',
        },
        '*': {
          '&:not(.MuiSvgIcon-root)': {
            color: '#0F172A !important',
          },
        },
        '.MuiTypography-root': {
          color: '#0F172A !important',
        },
        '.MuiTypography-body2': {
          color: '#475569 !important',
        },
      },
    },
    MuiCard: {
      styleOverrides: {
        root: {
          backgroundColor: '#FFFFFF !important',
          border: '1px solid #E2E8F0 !important',
          borderRadius: 12,
          boxShadow: '0 1px 3px rgba(0, 0, 0, 0.1), 0 1px 2px rgba(0, 0, 0, 0.06) !important',
          transition: 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)',
          '&:hover': {
            borderColor: '#1976D2 !important',
            boxShadow: '0 8px 25px rgba(25, 118, 210, 0.12), 0 4px 10px rgba(0, 0, 0, 0.08) !important',
            transform: 'translateY(-4px)',
          },
        },
      },
    },
    MuiPaper: {
      styleOverrides: {
        root: {
          backgroundColor: '#FFFFFF',
          border: '1px solid #E2E8F0',
          color: '#0F172A',
          boxShadow: '0 1px 3px rgba(0, 0, 0, 0.1), 0 1px 2px rgba(0, 0, 0, 0.06)',
        },
      },
    },
    MuiButton: {
      styleOverrides: {
        root: {
          borderRadius: 8,
          textTransform: 'none',
          fontWeight: 600,
          padding: '10px 20px',
          transition: 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)',
          '&:hover': {
            transform: 'translateY(-2px)',
          },
        },
        contained: {
          boxShadow: '0 2px 4px rgba(0, 0, 0, 0.1)',
          '&:hover': {
            boxShadow: '0 4px 12px rgba(0, 0, 0, 0.15)',
          },
        },
        containedPrimary: {
          background: 'linear-gradient(135deg, #1976D2 0%, #1565C0 100%)',
          '&:hover': {
            background: 'linear-gradient(135deg, #42A5F5 0%, #1976D2 100%)',
            boxShadow: '0 4px 12px rgba(25, 118, 210, 0.3)',
          },
        },
        containedSecondary: {
          background: 'linear-gradient(135deg, #7C3AED 0%, #5B21B6 100%)',
          '&:hover': {
            background: 'linear-gradient(135deg, #9F67FF 0%, #7C3AED 100%)',
            boxShadow: '0 4px 12px rgba(124, 58, 237, 0.3)',
          },
        },
      },
    },
    MuiChip: {
      styleOverrides: {
        root: {
          borderRadius: 8,
          fontWeight: 500,
        },
        colorPrimary: {
          background: 'linear-gradient(135deg, #1976D2 0%, #1565C0 100%)',
          color: '#FFFFFF',
        },
        colorSecondary: {
          background: 'linear-gradient(135deg, #7C3AED 0%, #5B21B6 100%)',
          color: '#FFFFFF',
        },
      },
    },
    MuiTextField: {
      styleOverrides: {
        root: {
          '& .MuiOutlinedInput-root': {
            backgroundColor: '#FFFFFF !important',
            borderRadius: 8,
            '& fieldset': {
              borderColor: '#E2E8F0 !important',
              borderWidth: '2px',
            },
            '&:hover fieldset': {
              borderColor: '#94A3B8 !important',
            },
            '&.Mui-focused fieldset': {
              borderColor: '#1976D2 !important',
              boxShadow: '0 0 0 3px rgba(25, 118, 210, 0.1)',
            },
            '& input': {
              color: '#0F172A !important',
              fontSize: '14px',
            },
            '& textarea': {
              color: '#0F172A !important',
              fontSize: '14px',
            },
          },
          '& .MuiInputLabel-root': {
            color: '#475569 !important',
            fontSize: '14px',
            '&.Mui-focused': {
              color: '#1976D2 !important',
            },
            '&.Mui-error': {
              color: '#DC2626 !important',
            },
          },
          '& .MuiFormHelperText-root': {
            color: '#64748B !important',
            fontSize: '12px',
          },
        },
      },
    },
    MuiSelect: {
      styleOverrides: {
        root: {
          backgroundColor: '#FFFFFF !important',
          color: '#0F172A !important',
          borderRadius: 8,
          '& .MuiOutlinedInput-notchedOutline': {
            borderColor: '#E2E8F0 !important',
            borderWidth: '2px',
          },
          '&:hover .MuiOutlinedInput-notchedOutline': {
            borderColor: '#94A3B8 !important',
          },
          '&.Mui-focused .MuiOutlinedInput-notchedOutline': {
            borderColor: '#1976D2 !important',
            boxShadow: '0 0 0 3px rgba(25, 118, 210, 0.1)',
          },
          '& .MuiSelect-select': {
            color: '#0F172A !important',
            fontSize: '14px',
          },
        },
      },
    },
    MuiFormControl: {
      styleOverrides: {
        root: {
          '& .MuiInputLabel-root': {
            color: '#475569 !important',
            fontSize: '14px',
            '&.Mui-focused': {
              color: '#1976D2 !important',
            },
          },
        },
      },
    },
    MuiSwitch: {
      styleOverrides: {
        root: {
          '& .MuiSwitch-switchBase.Mui-checked': {
            color: '#1976D2 !important',
            '& + .MuiSwitch-track': {
              backgroundColor: '#1976D2 !important',
            },
          },
          '& .MuiSwitch-track': {
            backgroundColor: '#CBD5E1 !important',
          },
        },
      },
    },
    MuiFormControlLabel: {
      styleOverrides: {
        root: {
          '& .MuiFormControlLabel-label': {
            color: '#0F172A !important',
            fontSize: '14px',
          },
        },
      },
    },
    MuiMenu: {
      styleOverrides: {
        paper: {
          backgroundColor: '#FFFFFF',
          border: '1px solid #E2E8F0',
          borderRadius: 8,
          boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)',
        },
      },
    },
    MuiMenuItem: {
      styleOverrides: {
        root: {
          color: '#0F172A',
          '&:hover': {
            backgroundColor: '#F1F5F9',
          },
          '&.Mui-selected': {
            backgroundColor: 'rgba(25, 118, 210, 0.08)',
            '&:hover': {
              backgroundColor: 'rgba(25, 118, 210, 0.12)',
            },
          },
        },
      },
    },
    MuiDialog: {
      styleOverrides: {
        paper: {
          backgroundColor: '#FFFFFF',
          border: '1px solid #E2E8F0',
          borderRadius: 12,
          boxShadow: '0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04)',
        },
      },
    },
    MuiAccordion: {
      styleOverrides: {
        root: {
          backgroundColor: '#FFFFFF',
          border: '1px solid #E2E8F0',
          '&:before': {
            display: 'none',
          },
          '&.Mui-expanded': {
            margin: 'auto',
          },
        },
      },
    },
    MuiTypography: {
      styleOverrides: {
        root: {
          color: '#0F172A !important',
        },
        h1: {
          color: '#0F172A !important',
          fontWeight: 700,
        },
        h2: {
          color: '#0F172A !important',
          fontWeight: 700,
        },
        h3: {
          color: '#0F172A !important',
          fontWeight: 600,
        },
        h4: {
          color: '#0F172A !important',
          fontWeight: 600,
        },
        h5: {
          color: '#0F172A !important',
          fontWeight: 600,
        },
        h6: {
          color: '#0F172A !important',
          fontWeight: 600,
        },
        body1: {
          color: '#0F172A !important',
        },
        body2: {
          color: '#475569 !important',
        },
      },
    },
    MuiCardContent: {
      styleOverrides: {
        root: {
          '& .MuiTypography-root': {
            color: '#0F172A !important',
          },
          '& .MuiTypography-body2': {
            color: '#475569 !important',
          },
          '& .MuiTypography-h6': {
            color: '#0F172A !important',
            fontWeight: 600,
          },
        },
      },
    },
    MuiAvatar: {
      styleOverrides: {
        root: {
          backgroundColor: '#1976D2',
          color: '#FFFFFF',
        },
      },
    },
    MuiBox: {
      styleOverrides: {
        root: {
          '& .MuiTypography-root': {
            color: '#0F172A !important',
          },
        },
      },
    },
    MuiTabs: {
      styleOverrides: {
        root: {
          '& .MuiTabs-indicator': {
            backgroundColor: '#1976D2 !important',
          },
        },
      },
    },
    MuiTab: {
      styleOverrides: {
        root: {
          color: '#64748B !important',
          fontSize: '14px',
          fontWeight: 500,
          '&.Mui-selected': {
            color: '#1976D2 !important',
            fontWeight: 600,
          },
          '&:hover': {
            color: '#1976D2 !important',
          },
        },
      },
    },
    MuiDivider: {
      styleOverrides: {
        root: {
          borderColor: '#E2E8F0 !important',
        },
      },
    },
    MuiList: {
      styleOverrides: {
        root: {
          '& .MuiListItem-root': {
            '& .MuiListItemText-primary': {
              color: '#0F172A !important',
              fontSize: '14px',
              fontWeight: 500,
            },
            '& .MuiListItemText-secondary': {
              color: '#64748B !important',
              fontSize: '12px',
            },
          },
        },
      },
    },
    MuiAlert: {
      styleOverrides: {
        root: {
          borderRadius: 8,
          border: '1px solid',
          '& .MuiAlert-message': {
            color: 'inherit !important',
          },
          '& .MuiTypography-root': {
            color: 'inherit !important',
          },
        },
        standardSuccess: {
          backgroundColor: 'rgba(16, 185, 129, 0.1) !important',
          borderColor: 'rgba(16, 185, 129, 0.2) !important',
          color: '#047857 !important',
        },
        standardError: {
          backgroundColor: 'rgba(220, 38, 38, 0.1) !important',
          borderColor: 'rgba(220, 38, 38, 0.2) !important',
          color: '#B91C1C !important',
        },
        standardWarning: {
          backgroundColor: 'rgba(217, 119, 6, 0.1) !important',
          borderColor: 'rgba(217, 119, 6, 0.2) !important',
          color: '#B45309 !important',
        },
        standardInfo: {
          backgroundColor: 'rgba(25, 118, 210, 0.1) !important',
          borderColor: 'rgba(25, 118, 210, 0.2) !important',
          color: '#1565C0 !important',
        },
      },
    },
    MuiLinearProgress: {
      styleOverrides: {
        root: {
          borderRadius: 4,
          backgroundColor: 'rgba(0, 0, 0, 0.08)',
        },
        bar: {
          borderRadius: 4,
          background: 'linear-gradient(90deg, #1976D2 0%, #1565C0 100%)',
        },
      },
    },
    MuiFab: {
      styleOverrides: {
        root: {
          background: 'linear-gradient(135deg, #1976D2 0%, #1565C0 100%)',
          boxShadow: '0 4px 12px rgba(25, 118, 210, 0.3)',
          '&:hover': {
            background: 'linear-gradient(135deg, #42A5F5 0%, #1976D2 100%)',
            boxShadow: '0 6px 20px rgba(25, 118, 210, 0.4)',
            transform: 'scale(1.05)',
          },
        },
      },
    },
    MuiAccordion: {
      styleOverrides: {
        root: {
          backgroundColor: '#FFFFFF !important',
          border: '1px solid #E2E8F0 !important',
          '&:before': {
            display: 'none',
          },
          '&.Mui-expanded': {
            margin: 'auto',
          },
        },
      },
    },
    MuiAccordionSummary: {
      styleOverrides: {
        root: {
          '& .MuiTypography-root': {
            color: '#0F172A !important',
            fontWeight: 500,
          },
        },
      },
    },
    MuiAccordionDetails: {
      styleOverrides: {
        root: {
          '& .MuiTypography-root': {
            color: '#0F172A !important',
          },
        },
      },
    },
    MuiTypography: {
      styleOverrides: {
        root: {
          color: '#0F172A !important',
        },
        h1: {
          color: '#0F172A !important',
          fontWeight: 700,
        },
        h2: {
          color: '#0F172A !important',
          fontWeight: 700,
        },
        h3: {
          color: '#0F172A !important',
          fontWeight: 600,
        },
        h4: {
          color: '#0F172A !important',
          fontWeight: 600,
        },
        h5: {
          color: '#0F172A !important',
          fontWeight: 600,
        },
        h6: {
          color: '#0F172A !important',
          fontWeight: 600,
        },
        body1: {
          color: '#0F172A !important',
        },
        body2: {
          color: '#475569 !important',
        },
        caption: {
          color: '#64748B !important',
        },
        subtitle1: {
          color: '#0F172A !important',
        },
        subtitle2: {
          color: '#475569 !important',
        },
      },
    },
    MuiCardContent: {
      styleOverrides: {
        root: {
          '& .MuiTypography-root': {
            color: '#0F172A !important',
          },
          '& .MuiTypography-body2': {
            color: '#475569 !important',
          },
          '& .MuiTypography-h6': {
            color: '#0F172A !important',
            fontWeight: 600,
          },
        },
      },
    },
    MuiAvatar: {
      styleOverrides: {
        root: {
          backgroundColor: '#1976D2 !important',
          color: '#FFFFFF !important',
        },
      },
    },
    MuiBox: {
      styleOverrides: {
        root: {
          '& .MuiTypography-root': {
            color: '#0F172A !important',
          },
        },
      },
    },
    MuiStepper: {
      styleOverrides: {
        root: {
          backgroundColor: 'transparent !important',
          '& .MuiStepLabel-label': {
            color: '#475569 !important',
            '&.Mui-active': {
              color: '#1976D2 !important',
            },
            '&.Mui-completed': {
              color: '#059669 !important',
            },
          },
        },
      },
    },
    MuiStep: {
      styleOverrides: {
        root: {
          '& .MuiStepIcon-root': {
            color: '#CBD5E1 !important',
            '&.Mui-active': {
              color: '#1976D2 !important',
            },
            '&.Mui-completed': {
              color: '#059669 !important',
            },
          },
        },
      },
    },
    MuiTooltip: {
      styleOverrides: {
        tooltip: {
          backgroundColor: '#1F2937 !important',
          color: '#FFFFFF !important',
          fontSize: '12px',
          borderRadius: 6,
        },
      },
    },
  },
};

function App() {
  const [backendStatus, setBackendStatus] = useState('connecting');
  const [currentPage, setCurrentPage] = useState('dashboard');
  const [isDarkMode, setIsDarkMode] = useState(true);
  
  // Initialize theme class on mount
  useEffect(() => {
    if (isDarkMode) {
      document.documentElement.classList.remove('light-mode');
    } else {
      document.documentElement.classList.add('light-mode');
    }
  }, []);
  const [botStatus, setBotStatus] = useState({
    isRunning: false,
    currentTask: null,
    progress: 0,
    lastUpdate: null,
  });

  // Create theme based on mode
  const theme = React.useMemo(() => {
    const baseTheme = createAppTheme(isDarkMode ? 'dark' : 'light');
    if (!isDarkMode) {
      return createTheme({
        ...baseTheme,
        ...lightThemeOverrides,
      });
    }
    return baseTheme;
  }, [isDarkMode]);

  useEffect(() => {
    // Check backend status
    const checkStatus = async () => {
      try {
        const status = await checkBackendStatus();
        setBackendStatus(status ? 'connected' : 'disconnected');
      } catch (error) {
        setBackendStatus('disconnected');
      }
    };

    checkStatus();
    const statusInterval = setInterval(checkStatus, 5000);

    // Connect WebSocket for real-time updates
    connectWebSocket((data) => {
      if (data.type === 'bot_status') {
        setBotStatus(data.payload);
      }
    });

    return () => {
      clearInterval(statusInterval);
      disconnectWebSocket();
    };
  }, []);

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Router>
        <Box sx={{ display: 'flex', height: '100vh', overflow: 'hidden' }}>
          {/* Sidebar */}
          <Sidebar 
            currentPage={currentPage} 
            onPageChange={setCurrentPage}
            backendStatus={backendStatus}
            isDarkMode={isDarkMode}
            onThemeToggle={() => {
              const newMode = !isDarkMode;
              setIsDarkMode(newMode);
              // Apply light-mode class to root element for CSS variables
              if (newMode) {
                document.documentElement.classList.remove('light-mode');
              } else {
                document.documentElement.classList.add('light-mode');
              }
            }}
          />
          
          {/* Main Content */}
          <Box sx={{ 
            flexGrow: 1, 
            display: 'flex', 
            flexDirection: 'column',
            overflow: 'hidden'
          }}>
            {/* Top Bar */}
            <TopBar 
              backendStatus={backendStatus}
              botStatus={botStatus}
              isDarkMode={isDarkMode}
            />
            
            {/* Page Content */}
            <Box sx={{ 
              flexGrow: 1, 
              overflow: 'auto',
              p: 3,
              background: isDarkMode ? `
                radial-gradient(circle at 20% 50%, rgba(0, 217, 255, 0.05) 0%, transparent 50%),
                radial-gradient(circle at 80% 20%, rgba(124, 58, 237, 0.05) 0%, transparent 50%),
                linear-gradient(135deg, rgba(0, 217, 255, 0.02) 0%, rgba(124, 58, 237, 0.02) 100%)
              ` : `
                radial-gradient(circle at 20% 50%, rgba(25, 118, 210, 0.04) 0%, transparent 70%),
                radial-gradient(circle at 80% 20%, rgba(124, 58, 237, 0.04) 0%, transparent 70%),
                radial-gradient(circle at 40% 80%, rgba(16, 185, 129, 0.03) 0%, transparent 60%),
                linear-gradient(135deg, rgba(248, 250, 252, 1) 0%, rgba(241, 245, 249, 1) 100%)
              `
            }}>
              <Routes>
                <Route path="/" element={
                  <Dashboard 
                    backendStatus={backendStatus}
                    botStatus={botStatus}
                    isDarkMode={isDarkMode}
                  />
                } />
                <Route path="/tasks" element={<TaskBuilder isDarkMode={isDarkMode} />} />
                <Route path="/monitor" element={
                  <LiveMonitor botStatus={botStatus} />
                } />
                <Route path="/settings" element={<Settings isDarkMode={isDarkMode} />} />
                <Route path="/results" element={<Results isDarkMode={isDarkMode} />} />
                <Route path="/unit-receiving" element={<UnitReceiving isDarkMode={isDarkMode} />} />
              </Routes>
            </Box>
          </Box>
        </Box>
      </Router>
      
      {/* Premium Toast Notifications */}
      <Toaster
        position="top-right"
        toastOptions={{
          duration: 4000,
          style: isDarkMode ? {
            background: 'rgba(22, 27, 34, 0.95)',
            color: '#F0F6FC',
            border: '1px solid #30363D',
            borderRadius: '12px',
            backdropFilter: 'blur(16px)',
            boxShadow: '0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05)',
            fontSize: '14px',
            fontWeight: 500,
          } : {
            background: 'rgba(255, 255, 255, 0.95)',
            color: '#0F172A',
            border: '1px solid #E2E8F0',
            borderRadius: '12px',
            backdropFilter: 'blur(16px)',
            boxShadow: '0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05)',
            fontSize: '14px',
            fontWeight: 500,
          },
          success: {
            style: {
              borderLeft: isDarkMode ? '4px solid #10B981' : '4px solid #059669',
            },
          },
          error: {
            style: {
              borderLeft: isDarkMode ? '4px solid #EF4444' : '4px solid #DC2626',
            },
          },
          loading: {
            style: {
              borderLeft: isDarkMode ? '4px solid #00D9FF' : '4px solid #1976D2',
            },
          },
        }}
      />
    </ThemeProvider>
  );
}

export default App;

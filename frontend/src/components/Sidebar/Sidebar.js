import React from 'react';
import {
  Box,
  Drawer,
  List,
  ListItem,
  ListItemButton,
  ListItemIcon,
  ListItemText,
  Typography,
  Chip,
  Divider,
  Avatar,
} from '@mui/material';
import {
  Dashboard as DashboardIcon,
  Build as BuildIcon,
  Visibility as MonitorIcon,
  Settings as SettingsIcon,
  Assessment as ResultsIcon,
  SmartToy as BotIcon,
  LightMode as LightModeIcon,
  DarkMode as DarkModeIcon,
  Assignment as RMAIcon,
} from '@mui/icons-material';
import { useNavigate, useLocation } from 'react-router-dom';

const DRAWER_WIDTH = 280;

const menuItems = [
  {
    id: 'dashboard',
    label: 'Dashboard',
    icon: DashboardIcon,
    path: '/',
    description: 'RMA Operations Overview'
  },
  {
    id: 'tasks',
    label: 'RMA Processing',
    icon: RMAIcon,
    path: '/tasks',
    description: 'Automated RMA Handling'
  },
  {
    id: 'monitor',
    label: 'Live Monitor',
    icon: MonitorIcon,
    path: '/monitor',
    description: 'Real-time Operations'
  },
  {
    id: 'results',
    label: 'Reports',
    icon: ResultsIcon,
    path: '/results',
    description: 'RMA Analytics & Data'
  },
  {
    id: 'settings',
    label: 'Settings',
    icon: SettingsIcon,
    path: '/settings',
    description: 'PLUS Integration'
  },
];

const Sidebar = ({ backendStatus, isDarkMode, onThemeToggle }) => {
  const navigate = useNavigate();
  const location = useLocation();

  const getStatusColor = (status) => {
    switch (status) {
      case 'connected':
        return 'success';
      case 'connecting':
        return 'warning';
      default:
        return 'error';
    }
  };

  const getStatusText = (status) => {
    switch (status) {
      case 'connected':
        return 'Online';
      case 'connecting':
        return 'Connecting...';
      default:
        return 'Offline';
    }
  };

  return (
    <Drawer
      variant="permanent"
      sx={{
        width: DRAWER_WIDTH,
        flexShrink: 0,
        '& .MuiDrawer-paper': {
          width: DRAWER_WIDTH,
          boxSizing: 'border-box',
          background: isDarkMode 
            ? 'linear-gradient(180deg, #2d2d2d 0%, #1a1a1a 100%)'
            : 'linear-gradient(180deg, #FFFFFF 0%, #F8FAFC 100%)',
          border: 'none',
          borderRight: isDarkMode 
            ? '1px solid rgba(255, 255, 255, 0.1)'
            : '1px solid #E2E8F0',
        },
      }}
    >
      {/* Header */}
      <Box sx={{ p: 3, textAlign: 'center' }}>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', mb: 2 }}>
          <Box sx={{ flexGrow: 1 }}>
            <Avatar
              sx={{
                width: 60,
                height: 60,
                margin: '0 auto 16px',
                background: 'linear-gradient(135deg, #1976D2 0%, #7C3AED 100%)',
              }}
            >
              <RMAIcon sx={{ fontSize: 32 }} />
            </Avatar>
          </Box>
          
          {/* Theme Toggle Button */}
          <Box
            onClick={onThemeToggle}
            sx={{
              cursor: 'pointer',
              p: 1,
              borderRadius: '50%',
              backgroundColor: isDarkMode ? 'rgba(255, 255, 255, 0.1)' : 'rgba(0, 0, 0, 0.1)',
              '&:hover': {
                backgroundColor: isDarkMode ? 'rgba(255, 255, 255, 0.2)' : 'rgba(0, 0, 0, 0.2)',
              },
              transition: 'all 0.2s ease',
            }}
          >
            {isDarkMode ? (
              <LightModeIcon sx={{ fontSize: 20, color: '#FFA726' }} />
            ) : (
              <DarkModeIcon sx={{ fontSize: 20, color: '#424242' }} />
            )}
          </Box>
        </Box>
        
        <Typography variant="h6" sx={{ fontWeight: 600, mb: 1 }}>
          Reconext ADT Bot
        </Typography>
        
        <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
          Intelligent RMA Processing
        </Typography>
        
        <Chip
          label={getStatusText(backendStatus)}
          color={getStatusColor(backendStatus)}
          size="small"
          sx={{ fontWeight: 500 }}
        />
      </Box>

      <Divider sx={{ borderColor: isDarkMode ? 'rgba(255, 255, 255, 0.1)' : 'rgba(0, 0, 0, 0.1)' }} />

      {/* Navigation Menu */}
      <Box sx={{ flexGrow: 1, px: 2, py: 1 }}>
        <List>
          {menuItems.map((item) => {
            const Icon = item.icon;
            const isActive = location.pathname === item.path;
            
            return (
              <ListItem key={item.id} disablePadding sx={{ mb: 0.5 }}>
                <ListItemButton
                  onClick={() => navigate(item.path)}
                  sx={{
                    borderRadius: 2,
                    py: 1.5,
                    px: 2,
                    backgroundColor: isActive 
                      ? (isDarkMode ? 'rgba(102, 126, 234, 0.15)' : 'rgba(25, 118, 210, 0.1)')
                      : 'transparent',
                    border: isActive 
                      ? (isDarkMode ? '1px solid rgba(102, 126, 234, 0.3)' : '1px solid rgba(25, 118, 210, 0.3)')
                      : '1px solid transparent',
                    '&:hover': {
                      backgroundColor: isActive 
                        ? (isDarkMode ? 'rgba(102, 126, 234, 0.2)' : 'rgba(25, 118, 210, 0.15)')
                        : (isDarkMode ? 'rgba(255, 255, 255, 0.05)' : 'rgba(0, 0, 0, 0.05)'),
                      transform: 'translateX(4px)',
                    },
                    transition: 'all 0.2s ease',
                  }}
                >
                  <ListItemIcon
                    sx={{
                      color: isActive ? (isDarkMode ? '#667eea' : '#1976D2') : 'text.secondary',
                      minWidth: 40,
                    }}
                  >
                    <Icon />
                  </ListItemIcon>
                  
                  <ListItemText
                    primary={item.label}
                    secondary={item.description}
                    primaryTypographyProps={{
                      fontWeight: isActive ? 600 : 500,
                      color: isActive ? (isDarkMode ? '#667eea' : '#1976D2') : 'text.primary',
                    }}
                    secondaryTypographyProps={{
                      fontSize: '0.75rem',
                      color: 'text.secondary',
                    }}
                  />
                </ListItemButton>
              </ListItem>
            );
          })}
        </List>
      </Box>

      {/* Footer */}
      <Box sx={{ p: 2, textAlign: 'center' }}>
        <Typography variant="caption" color="text.secondary">
          Version 2.0.0
        </Typography>
      </Box>
    </Drawer>
  );
};

export default Sidebar;

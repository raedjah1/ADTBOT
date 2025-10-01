import React from 'react';
import {
  AppBar,
  Toolbar,
  Typography,
  Box,
  IconButton,
  Chip,
  LinearProgress,
  Tooltip,
} from '@mui/material';
import {
  PlayArrow as PlayIcon,
  Stop as StopIcon,
  Pause as PauseIcon,
} from '@mui/icons-material';

const TopBar = ({ backendStatus, botStatus, isDarkMode }) => {

  const getBotStatusColor = () => {
    if (!botStatus.isRunning) return 'default';
    if (botStatus.currentTask) return 'success';
    return 'warning';
  };

  const getBotStatusText = () => {
    if (!botStatus.isRunning) return 'Idle';
    if (botStatus.currentTask) return 'Running Task';
    return 'Ready';
  };

  return (
    <AppBar
      position="static"
      elevation={0}
      sx={{
        backgroundColor: isDarkMode 
          ? 'rgba(45, 45, 45, 0.95)' 
          : 'rgba(255, 255, 255, 0.98)',
        backdropFilter: 'blur(10px)',
        borderBottom: isDarkMode 
          ? '1px solid rgba(255, 255, 255, 0.1)'
          : '1px solid rgba(226, 232, 240, 0.8)',
        color: isDarkMode ? '#F0F6FC' : '#0F172A',
      }}
    >
      <Toolbar sx={{ 
        minHeight: '64px !important', 
        px: 3,
        '& .MuiTypography-root': {
          color: isDarkMode ? '#F0F6FC' : '#0F172A !important',
        },
        '& .MuiChip-root': {
          backgroundColor: isDarkMode ? 'rgba(255, 255, 255, 0.1)' : 'rgba(25, 118, 210, 0.1)',
          color: isDarkMode ? '#F0F6FC' : '#1976D2',
        },
      }}>
        {/* Left Section - Bot Status */}
        <Box sx={{ display: 'flex', alignItems: 'center', flexGrow: 1 }}>
          <Chip
            label={getBotStatusText()}
            color={getBotStatusColor()}
            size="small"
            sx={{ mr: 2, fontWeight: 500 }}
          />
          
          {botStatus.currentTask && (
            <Box sx={{ display: 'flex', alignItems: 'center', ml: 2 }}>
              <Typography variant="body2" sx={{ mr: 1 }}>
                Processing: {botStatus.currentTask}
              </Typography>
              <Box sx={{ width: 100, mr: 1 }}>
                <LinearProgress
                  variant="determinate"
                  value={botStatus.progress || 0}
                  sx={{
                    height: 4,
                    borderRadius: 2,
                    backgroundColor: isDarkMode 
                      ? 'rgba(255, 255, 255, 0.1)'
                      : 'rgba(0, 0, 0, 0.1)',
                    '& .MuiLinearProgress-bar': {
                      background: isDarkMode
                        ? 'linear-gradient(90deg, #667eea 0%, #764ba2 100%)'
                        : 'linear-gradient(90deg, #1976D2 0%, #1565C0 100%)',
                    },
                  }}
                />
              </Box>
              <Typography variant="caption" color="text.secondary">
                {Math.round(botStatus.progress || 0)}%
              </Typography>
            </Box>
          )}
        </Box>

        {/* Center Section - Current Time */}
        <Box sx={{ textAlign: 'center', mx: 2 }}>
          <Typography variant="body2" color="text.secondary">
            {new Date().toLocaleTimeString()}
          </Typography>
        </Box>

        {/* Right Section - System Status */}
        <Box sx={{ display: 'flex', alignItems: 'center' }}>
          <Chip
            label={backendStatus === 'connected' ? 'System Online' : 'System Offline'}
            color={backendStatus === 'connected' ? 'success' : 'error'}
            size="small"
            sx={{ fontWeight: 500 }}
          />
        </Box>
      </Toolbar>
    </AppBar>
  );
};

export default TopBar;

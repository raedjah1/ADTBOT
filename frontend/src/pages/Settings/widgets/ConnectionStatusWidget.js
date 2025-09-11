import React from 'react';
import {
  Box,
  Typography,
  Button,
  Chip,
  Paper,
} from '@mui/material';
import {
  CheckCircle,
  Refresh as RefreshIcon,
  Cloud as CloudIcon,
} from '@mui/icons-material';

const ConnectionStatusWidget = ({ baseUrl, username, password, onTestConnection }) => {
  const isReady = baseUrl && username && password;

  return (
    <Paper 
      elevation={1}
      sx={{ 
        p: 3, 
        textAlign: 'center',
        background: (theme) => theme.palette.mode === 'dark' 
          ? 'linear-gradient(135deg, #1a1a2e 0%, #16213e 100%)'
          : 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
        color: 'white',
      }}
    >
      <CloudIcon sx={{ fontSize: 48, mb: 2, opacity: 0.9 }} />
      
      <Typography variant="h6" sx={{ mb: 2, fontWeight: 600 }}>
        Connection Status
      </Typography>
      
      <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'center', mb: 3 }}>
        <CheckCircle 
          sx={{ 
            mr: 1,
            color: isReady ? '#4caf50' : 'rgba(255,255,255,0.5)'
          }} 
        />
        <Chip 
          label={isReady ? "Ready to Test" : "Not Configured"} 
          sx={{
            backgroundColor: isReady ? 'rgba(76, 175, 80, 0.2)' : 'rgba(255,255,255,0.2)',
            color: 'white',
            fontWeight: 500,
          }}
        />
      </Box>
      
      <Button 
        variant="contained"
        onClick={onTestConnection}
        startIcon={<RefreshIcon />}
        disabled={!isReady}
        sx={{
          backgroundColor: 'rgba(255,255,255,0.2)',
          color: 'white',
          fontWeight: 600,
          '&:hover': {
            backgroundColor: 'rgba(255,255,255,0.3)',
          },
          '&:disabled': {
            backgroundColor: 'rgba(255,255,255,0.1)',
            color: 'rgba(255,255,255,0.5)',
          }
        }}
      >
        Test Connection
      </Button>
    </Paper>
  );
};

export default ConnectionStatusWidget;

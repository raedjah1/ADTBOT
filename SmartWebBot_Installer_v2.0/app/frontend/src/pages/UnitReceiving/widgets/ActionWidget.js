import React from 'react';
import {
  Card,
  CardContent,
  Typography,
  Button,
  Alert,
  CircularProgress,
} from '@mui/material';
import {
  PlayArrow as StartIcon,
} from '@mui/icons-material';

const ActionWidget = ({ 
  isLoading, 
  statusMessage, 
  onBeginUnitReceiving 
}) => {
  return (
    <Card>
      <CardContent sx={{ p: 4, textAlign: 'center' }}>
        <Typography variant="h6" sx={{ fontWeight: 600, mb: 2 }}>
          Begin Unit Receiving Process
        </Typography>
        
        <Typography variant="body2" color="text.secondary" sx={{ mb: 4, maxWidth: 500, mx: 'auto' }}>
          Start the automated unit receiving process for ADT program. 
          This will handle incoming units, validate serial numbers, and update inventory status.
        </Typography>

        {/* Status Message */}
        {statusMessage && (
          <Alert 
            severity={
              statusMessage.includes('✗') || statusMessage.includes('failed') || statusMessage.includes('error') ? 'error' : 
              statusMessage.includes('Redirecting') ? 'warning' :
              statusMessage.includes('✓') || statusMessage.includes('successful') ? 'success' :
              'info'
            }
            sx={{ mb: 3, maxWidth: 600, mx: 'auto' }}
          >
            {statusMessage}
          </Alert>
        )}

        {/* Main Action Button */}
        <Button
          variant="contained"
          size="large"
          startIcon={isLoading ? <CircularProgress size={20} color="inherit" /> : <StartIcon />}
          onClick={onBeginUnitReceiving}
          disabled={isLoading}
          sx={{
            py: 2,
            px: 4,
            fontSize: '1.1rem',
            fontWeight: 600,
            background: 'linear-gradient(135deg, #00D9FF 0%, #7C3AED 100%)',
            '&:hover': {
              background: 'linear-gradient(135deg, #33E1FF 0%, #9F67FF 100%)',
              transform: 'translateY(-2px)',
              boxShadow: '0 8px 25px rgba(0, 217, 255, 0.3)',
            },
            '&:disabled': {
              background: 'rgba(0, 0, 0, 0.12)',
            },
          }}
        >
          {isLoading ? (
            statusMessage.includes('login') ? 'Logging in...' :
            statusMessage.includes('Navigating') ? 'Navigating...' :
            'Processing...'
          ) : 'Begin Unit Receiving'}
        </Button>

        {/* Info Text */}
        <Typography variant="caption" color="text.secondary" sx={{ display: 'block', mt: 2 }}>
          Will automatically login to PLUS if needed, then navigate to Unit Receiving ADT
        </Typography>
      </CardContent>
    </Card>
  );
};

export default ActionWidget;

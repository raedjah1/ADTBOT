import React from 'react';
import {
  Box,
  Paper,
  Typography,
  Chip,
  Stack,
  IconButton,
  Tooltip,
} from '@mui/material';
import {
  Inventory as InventoryIcon,
  CheckCircle as CheckIcon,
  Error as ErrorIcon,
  Settings as SettingsIcon,
} from '@mui/icons-material';
import { useNavigate } from 'react-router-dom';

const HeaderWidget = ({ isDarkMode, plusStatus }) => {
  const navigate = useNavigate();

  const getStatusIcon = () => {
    if (plusStatus?.is_logged_in) {
      return <CheckIcon sx={{ color: 'success.main' }} />;
    }
    return <ErrorIcon sx={{ color: 'error.main' }} />;
  };

  const getStatusColor = () => {
    if (plusStatus?.is_logged_in) {
      return 'success';
    }
    return 'error';
  };

  const getStatusText = () => {
    if (plusStatus?.is_logged_in) {
      return 'Connected';
    }
    return 'Not Connected';
  };

  return (
    <Paper
      elevation={0}
      sx={{
        p: 4,
        mb: 4,
        background: isDarkMode
          ? 'linear-gradient(135deg, rgba(0, 217, 255, 0.1) 0%, rgba(124, 58, 237, 0.1) 100%)'
          : 'linear-gradient(135deg, rgba(25, 118, 210, 0.1) 0%, rgba(124, 58, 237, 0.1) 100%)',
        border: isDarkMode ? '1px solid #30363D' : '1px solid #E2E8F0',
        borderRadius: 3,
      }}
    >
      <Stack direction="row" alignItems="center" spacing={3}>
        <Box
          sx={{
            p: 2,
            borderRadius: 2,
            background: 'linear-gradient(135deg, #00D9FF 0%, #7C3AED 100%)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
          }}
        >
          <InventoryIcon sx={{ fontSize: 40, color: 'white' }} />
        </Box>
        
        <Box sx={{ flex: 1 }}>
          <Typography variant="h4" sx={{ fontWeight: 700, mb: 1 }}>
            Unit Receiving ADT
          </Typography>
          <Typography variant="body1" color="text.secondary">
            Automated unit receiving and processing for ADT program
          </Typography>
        </Box>
        
        {/* Settings & Status Section */}
        <Stack direction="row" alignItems="center" spacing={2}>
          {/* Part Mapping Settings Icon */}
          <Tooltip title="Manage Part Number Mappings">
            <IconButton
              onClick={() => navigate('/settings/part-mappings')}
              sx={{
                p: 2,
                borderRadius: 2,
                background: 'rgba(124, 58, 237, 0.1)',
                border: '1px solid rgba(124, 58, 237, 0.2)',
                '&:hover': {
                  background: 'rgba(124, 58, 237, 0.2)',
                  transform: 'translateY(-2px)',
                  boxShadow: '0 8px 16px rgba(124, 58, 237, 0.2)',
                },
                transition: 'all 0.3s ease',
              }}
            >
              <SettingsIcon sx={{ color: '#7C3AED', fontSize: 28 }} />
            </IconButton>
          </Tooltip>

          {/* PLUS Status Indicator */}
          <Box sx={{ textAlign: 'center' }}>
            <Typography variant="caption" color="text.secondary" sx={{ display: 'block', mb: 1 }}>
              PLUS Status
            </Typography>
            <Chip
              icon={getStatusIcon()}
              label={getStatusText()}
              color={getStatusColor()}
              variant="outlined"
              sx={{ fontWeight: 600 }}
            />
          </Box>
        </Stack>
      </Stack>
    </Paper>
  );
};

export default HeaderWidget;

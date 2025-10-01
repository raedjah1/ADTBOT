import React from 'react';
import {
  Card,
  CardContent,
  Typography,
  Chip,
  Stack,
  Box,
  Divider,
} from '@mui/material';

const SystemStatusWidget = ({ plusStatus }) => {
  return (
    <Card>
      <CardContent sx={{ p: 4 }}>
        <Typography variant="h6" sx={{ fontWeight: 600, mb: 3 }}>
          System Status
        </Typography>
        
        <Stack spacing={2}>
          <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <Typography variant="body2" color="text.secondary">
              PLUS Connection
            </Typography>
            <Chip
              size="small"
              label={plusStatus?.is_logged_in ? 'Connected' : 'Disconnected'}
              color={plusStatus?.is_logged_in ? 'success' : 'error'}
            />
          </Box>
          
          <Divider />
          
          <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <Typography variant="body2" color="text.secondary">
              ADT Program Access
            </Typography>
            <Chip
              size="small"
              label={plusStatus?.is_logged_in ? 'Available' : 'Unavailable'}
              color={plusStatus?.is_logged_in ? 'success' : 'default'}
            />
          </Box>
          
          <Divider />
          
          <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <Typography variant="body2" color="text.secondary">
              Unit Processing
            </Typography>
            <Chip
              size="small"
              label="Ready"
              color="info"
            />
          </Box>
        </Stack>
      </CardContent>
    </Card>
  );
};

export default SystemStatusWidget;

import React from 'react';
import { Box, Typography, Card, CardContent } from '@mui/material';

const LiveMonitor = ({ botStatus }) => {
  return (
    <Box>
      <Typography variant="h4" sx={{ fontWeight: 600, mb: 3 }}>
        Live Monitor 📺
      </Typography>
      
      <Card className="glass-effect">
        <CardContent>
          <Typography variant="h6" sx={{ mb: 2 }}>
            Real-time Bot Monitoring
          </Typography>
          <Typography color="text.secondary">
            Live screenshots and step-by-step progress tracking will appear here.
          </Typography>
        </CardContent>
      </Card>
    </Box>
  );
};

export default LiveMonitor;

import React from 'react';
import {
  Card,
  CardContent,
  Typography,
  Stack,
  Box,
} from '@mui/material';

const ProcessOverviewWidget = () => {
  const processSteps = [
    'Verify PLUS connection and ADT program access',
    'Scan and validate incoming unit serial numbers',
    'Update inventory status and location tracking',
    'Generate receiving reports and notifications'
  ];

  return (
    <Card>
      <CardContent sx={{ p: 4 }}>
        <Typography variant="h6" sx={{ fontWeight: 600, mb: 3 }}>
          Process Overview
        </Typography>
        
        <Stack spacing={2}>
          {processSteps.map((step, index) => (
            <Box key={index} sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
              <Box
                sx={{
                  width: 8,
                  height: 8,
                  borderRadius: '50%',
                  backgroundColor: 'primary.main',
                }}
              />
              <Typography variant="body2">
                {step}
              </Typography>
            </Box>
          ))}
        </Stack>
      </CardContent>
    </Card>
  );
};

export default ProcessOverviewWidget;

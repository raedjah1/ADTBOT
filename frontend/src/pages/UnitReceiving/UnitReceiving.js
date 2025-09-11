import React from 'react';
import {
  Box,
  Container,
  Stack,
} from '@mui/material';

// Components
import {
  HeaderWidget,
  SystemStatusWidget,
  ActionWidget,
  ProcessOverviewWidget,
} from './widgets';

// Hooks
import { usePlusStatus } from './hooks';

const UnitReceiving = ({ isDarkMode }) => {
  const {
    plusStatus,
    isLoading,
    statusMessage,
    handleBeginUnitReceiving,
  } = usePlusStatus();

  return (
    <Container maxWidth="lg">
      <Box sx={{ py: 4 }}>
        {/* Header */}
        <HeaderWidget isDarkMode={isDarkMode} plusStatus={plusStatus} />

        {/* Main Content */}
        <Stack spacing={4}>
          {/* System Status Card */}
          <SystemStatusWidget plusStatus={plusStatus} />

          {/* Action Card */}
          <ActionWidget 
            isLoading={isLoading}
            statusMessage={statusMessage}
            onBeginUnitReceiving={handleBeginUnitReceiving}
          />

          {/* Process Overview Card */}
          <ProcessOverviewWidget />
        </Stack>
      </Box>
    </Container>
  );
};

export default UnitReceiving;

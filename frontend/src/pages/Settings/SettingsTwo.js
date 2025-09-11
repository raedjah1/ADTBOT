import React, { useState } from 'react';
import {
  Box,
  Typography,
  Tabs,
  Tab,
  Paper,
} from '@mui/material';
import {
  Security as SecurityIcon,
  Settings as SettingsIcon,
  Notifications as NotificationIcon,
  Cloud as CloudIcon,
} from '@mui/icons-material';

// Import our widget components
import PlusIntegrationWidget from './widgets/PlusIntegrationWidget';
import RmaProcessingWidget from './widgets/RmaProcessingWidget';
import NotificationWidget from './widgets/NotificationWidget';
import PerformanceWidget from './widgets/PerformanceWidget';

const Settings = ({ isDarkMode = true }) => {
  const [activeTab, setActiveTab] = useState(0);

  const TabPanel = ({ children, value, index }) => (
    <div hidden={value !== index}>
      {value === index && <Box sx={{ py: 3 }}>{children}</Box>}
    </div>
  );

  return (
    <Box sx={{ p: 4, maxWidth: 1400, mx: 'auto' }}>
      {/* Header */}
      <Box sx={{ mb: 4 }}>
        <Typography variant="h4" sx={{ mb: 1, fontWeight: 700, color: 'primary.main' }}>
          System Settings
        </Typography>
        <Typography variant="h6" color="text.secondary">
          Configure your SmartWebBot for optimal performance
        </Typography>
      </Box>

      {/* Main Settings Card */}
      <Paper elevation={2} sx={{ borderRadius: 2 }}>
        {/* Tabs */}
        <Box sx={{ borderBottom: 1, borderColor: 'divider' }}>
          <Tabs 
            value={activeTab} 
            onChange={(e, newValue) => setActiveTab(newValue)}
            sx={{ px: 2 }}
          >
            <Tab icon={<SecurityIcon />} iconPosition="start" label="PLUS Integration" />
            <Tab icon={<SettingsIcon />} iconPosition="start" label="RMA Processing" />
            <Tab icon={<NotificationIcon />} iconPosition="start" label="Notifications" />
            <Tab icon={<CloudIcon />} iconPosition="start" label="Performance" />
          </Tabs>
        </Box>

        {/* Tab Content */}
        <Box sx={{ p: 3 }}>
          <TabPanel value={activeTab} index={0}>
            <PlusIntegrationWidget isDarkMode={isDarkMode} />
          </TabPanel>

          <TabPanel value={activeTab} index={1}>
            <RmaProcessingWidget isDarkMode={isDarkMode} />
          </TabPanel>

          <TabPanel value={activeTab} index={2}>
            <NotificationWidget isDarkMode={isDarkMode} />
          </TabPanel>

          <TabPanel value={activeTab} index={3}>
            <PerformanceWidget isDarkMode={isDarkMode} />
          </TabPanel>
        </Box>
      </Paper>
    </Box>
  );
};

export default Settings;
